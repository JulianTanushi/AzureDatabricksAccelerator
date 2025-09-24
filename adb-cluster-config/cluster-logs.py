from pyspark.sql.functions import col, avg

# Example: load Spark metrics logs (replace with your logging path or table)
metrics_df = spark.read.json("dbfs:/cluster-logs/metrics/*.json")

# Calculate average CPU per executor
executor_util = (
    metrics_df
    .filter(col("metric") == "executorCpuTime")
    .groupBy("executorId")
    .agg(avg("value").alias("avg_cpu"))
)

# Calculate driver CPU usage
driver_util = (
    metrics_df
    .filter((col("metric") == "jvmCpuTime") & (col("executorId") == "driver"))
    .agg(avg("value").alias("driver_cpu"))
)

# Join with job metadata
# Suppose you have a job_runs table with job_id, cluster_id, runtime_seconds, etc.
job_runs = spark.read.table("monitoring.job_runs")

report = (
    job_runs
    .join(executor_util, job_runs.cluster_id == executor_util.executorId, "left")
    .join(driver_util)
)

# Heuristic flags
report = report.withColumn(
    "oversized_flag",
    (col("avg_cpu") < 0.1) & (col("runtime_seconds") > 300)  # workers idle + long run
).withColumn(
    "driver_bound_flag",
    (col("driver_cpu") > 0.7) & (col("avg_cpu") < 0.2)
)

display(report.select("job_id", "cluster_id", "oversized_flag", "driver_bound_flag"))