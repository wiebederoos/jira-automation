import os
import requests
import json
import logging
from constants import CREATE_ISSUE_URL, EPICS_DIRECTORY, JIRA_PROJECT_KEY, JIRA_BASE_URL
from auth import jira_auth, HEADERS, AUTH

def get_issue_fields(issue_key):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    params = {
        "fields": "*all",
        "expand": "names,schema"
    }

    response = requests.get(url, headers=HEADERS, auth=AUTH, params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None

    return response.json()

if __name__ == "__main__":
    issue_key = input("Enter the Jira issue key to fetch all of the fields: ").strip()
    jira_auth()
    epic = get_issue_fields(issue_key)
    if epic:
        # Pretty print JSON to console
        logging.info(json.dumps(epic, indent=2))
        
        # Save to file
        with open(f"{issue_key}_fields.json", "w", encoding="utf-8") as f:
            json.dump(epic, f, indent=2)
        logging.info(f"\n✅ All fields for {issue_key} saved to {issue_key}_fields.json")
