# This script uses the Databricks Jobs API to:
# 	•	List all jobs in the workspace,
# 	•	Check if timeout_seconds and email_notifications are set,
# 	•	Patch jobs that are missing them.

# You’ll need:
# 	•	A Databricks personal access token (PAT) or service principal token,
# 	•	The workspace URL (like https://<your-workspace>.azuredatabricks.net).

import requests # for making HTTP requests

# === CONFIG ===
DATABRICKS_INSTANCE = "https://<your-workspace>.azuredatabricks.net" # e.g. https://adb-1234567890123456
TOKEN = "<your-personal-access-token>"
DEFAULT_TIMEOUT = 7200  # 2h
DEFAULT_EMAILS = ["notifications@microsoft.com"]

headers = {"Authorization": f"Bearer {TOKEN}"}

def list_jobs():
    jobs = []
    has_more = True
    offset = 0
    while has_more:
        resp = requests.get(
            f"{DATABRICKS_INSTANCE}/api/2.1/jobs/list?offset={offset}", headers=headers
        ).json()
        jobs.extend(resp.get("jobs", []))
        has_more = resp.get("has_more", False)
        offset += len(resp.get("jobs", []))
    return jobs

def patch_job(job):
    job_id = job["job_id"]
    settings = job["settings"]

    # Add timeout if missing
    if not settings.get("timeout_seconds"):
        settings["timeout_seconds"] = DEFAULT_TIMEOUT

    # Add email notifications if missing
    notifications = settings.get("email_notifications", {})
    if not notifications.get("on_failure"):
        notifications["on_failure"] = DEFAULT_EMAILS
    if not notifications.get("on_success"):
        notifications["on_success"] = DEFAULT_EMAILS

    payload = {"job_id": job_id, "new_settings": settings}
    resp = requests.post(
        f"{DATABRICKS_INSTANCE}/api/2.1/jobs/update", headers=headers, json=payload
    )

    if resp.status_code == 200:
        print(f"Job {job_id} updated")
    else:
        print(f"Failed to update job {job_id}: {resp.text}")

if __name__ == "__main__":
    jobs = list_jobs()
    for job in jobs:
        patch_job(job)