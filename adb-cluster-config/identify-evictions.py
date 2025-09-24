# The following notebook analyzes spot instance eviction events in Databricks clusters and correlates them with job run durations to identify potential performance impacts. 
# The notebook performs the following steps:
# 	1.	Pulls cluster events → detects spot eviction events.
# 	2.	Pulls job runs for the same period.
# 	3.	Joins runs to clusters by cluster_instance.cluster_id.
# 	4.	Flags runs that had spot evictions.
# 	5.	Reports run duration vs. median baseline (to see if they ran longer).



import requests
import pandas as pd
from datetime import datetime, timedelta
from statistics import median

# === CONFIG ===
DATABRICKS_INSTANCE = "https://<your-workspace>.azuredatabricks.net"
TOKEN = "<your-personal-access-token>"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

LOOKBACK_DAYS = 7
SINCE_MS = int((datetime.now() - timedelta(days=LOOKBACK_DAYS)).timestamp() * 1000)


# --- Cluster Events ---
def get_cluster_events(cluster_id):
    events, offset, has_more = [], 0, True
    while has_more:
        resp = requests.get(
            f"{DATABRICKS_INSTANCE}/api/2.0/clusters/events",
            headers=HEADERS,
            params={"cluster_id": cluster_id, "offset": offset, "limit": 50},
        )
        resp.raise_for_status()
        data = resp.json()
        events.extend(data.get("events", []))
        has_more = data.get("has_more", False)
        offset += len(data.get("events", []))
    return events


# --- List Clusters ---
clusters = requests.get(f"{DATABRICKS_INSTANCE}/api/2.0/clusters/list", headers=HEADERS).json().get("clusters", [])


# --- Collect Spot Evictions ---
evictions = []
for c in clusters:
    cluster_id = c["cluster_id"]
    events = get_cluster_events(cluster_id)
    for e in events:
        ts = e.get("timestamp", 0)
        if ts < SINCE_MS:
            continue
        if "INSTANCE_TERMINATED_BY_SPOT" in str(e.get("details", {})):
            evictions.append({
                "cluster_id": cluster_id,
                "timestamp": datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M:%S"),
                "event_type": e.get("type"),
                "details": str(e.get("details"))
            })
evictions_df = pd.DataFrame(evictions)


# --- Job Runs ---
def list_runs():
    runs, has_more, offset = [], True, 0
    while has_more:
        resp = requests.get(
            f"{DATABRICKS_INSTANCE}/api/2.1/jobs/runs/list",
            headers=HEADERS,
            params={"limit": 50, "offset": offset, "completed_only": "true"},
        )
        resp.raise_for_status()
        data = resp.json()
        runs.extend(data.get("runs", []))
        has_more = len(data.get("runs", [])) == 50
        offset += 50
    return runs


runs = list_runs()
job_runs = []
for r in runs:
    if r.get("start_time", 0) < SINCE_MS:
        continue
    cluster = r.get("cluster_instance", {})
    job_runs.append({
        "run_id": r["run_id"],
        "job_id": r.get("job_id"),
        "cluster_id": cluster.get("cluster_id"),
        "start_time": datetime.fromtimestamp(r["start_time"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
        "duration_sec": r.get("run_duration", 0) / 1000,
        "state": r.get("state", {}).get("life_cycle_state")
    })

runs_df = pd.DataFrame(job_runs)


# --- Correlate Runs with Evictions ---
if not evictions_df.empty and not runs_df.empty:
    merged = runs_df.merge(evictions_df, on="cluster_id", how="left", indicator=True)
    merged["eviction_affected"] = merged["_merge"] == "both"

    # Compute median runtime per job (excluding eviction-affected runs)
    baseline = (
        merged[~merged["eviction_affected"]]
        .groupby("job_id")["duration_sec"]
        .median()
        .reset_index()
        .rename(columns={"duration_sec": "baseline_median_sec"})
    )

    merged = merged.merge(baseline, on="job_id", how="left")
    merged["runtime_delta_sec"] = merged["duration_sec"] - merged["baseline_median_sec"]

    display(merged.sort_values(["job_id", "start_time"]))
else:
    print("No evictions or job runs detected in the last period.")


#Automate evictions data to Delta Table and setup a scheduled job to run this notebook daily.


# --- Step1: Save Results to Delta Table ---
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

# Convert pandas -> Spark DataFrame
spark_df = spark.createDataFrame(merged)

# Save to Delta (append daily results)
spark_df.write.format("delta").mode("append").saveAsTable("monitoring.spot_eviction_impact")

# --- Step2: Schedule Notebook ---
# 1. In Databricks, go to "Jobs" and create a new job
# 2. Add a new task and select "Notebook"
# 3. Select this notebook and set the schedule to run daily at your preferred time
# 4. Configure notifications if needed to alert on failures or successes
# 5. Save the job configuration and enable it  to start running as per the schedule
# 6. Monitor the job runs and review the results in the Delta table
# 7. Optionally, create dashboards or alerts based on the data in the Delta table to monitor spot eviction impacts over time. (see code below)

# ---Step3: CREATE OR REPLACE VIEW monitoring.spot_eviction_summary AS
# SELECT 
#   job_id,
#   COUNT(*) AS runs,
#   SUM(CASE WHEN eviction_affected THEN 1 ELSE 0 END) AS eviction_runs,
#   ROUND(100 * SUM(CASE WHEN eviction_affected THEN 1 ELSE 0 END) / COUNT(*), 2) AS eviction_rate_pct,
#   ROUND(AVG(runtime_delta_sec),2) AS avg_runtime_delta_sec
# FROM monitoring.spot_eviction_impact
# GROUP BY job_id;

# SELECT * FROM monitoring.spot_eviction_summary ORDER BY eviction_rate_pct DESC;
# This view can be used to create dashboards or alerts in Databricks or other BI tools.

#Step4: Create Alerts (Optional)
# 1. In Databricks, navigate to the "Alerts" section.
# 2. Create a new alert based on the "monitoring.spot_eviction_summary" view.
# 3. Set conditions to trigger alerts, such as when the eviction_rate_pct exceeds a certain threshold.
# 4. Configure notification channels (email, Slack, etc.) to receive alerts
# 5. Save and enable the alert to start monitoring spot eviction impacts in real-time.

# Alternatively, you can push the results to Azure Monitor for centralized monitoring and alerting:
# Push to Azure Monitor
# 	•	Use the Azure Databricks → Log Analytics connector to export Delta table results.
# 	•	Then alert in Azure Monitor or Log Analytics with custom KQL queries.




