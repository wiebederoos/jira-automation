import os
import requests
import json
import logging
from constants import CREATE_ISSUE_URL, EPICS_DIRECTORY, JIRA_PROJECT_KEY, JIRA_BASE_URL
from auth import jira_auth, HEADERS, AUTH

JIRA_EPIC_KEY = "ECS-35"

def get_epic_fields(epic_key):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{epic_key}"
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
    jira_auth()
    epic = get_epic_fields(JIRA_EPIC_KEY)
    if epic:
        # Pretty print JSON to console
        logging.info(json.dumps(epic, indent=2))
        
        # Save to file
        with open(f"{JIRA_EPIC_KEY}_fields.json", "w", encoding="utf-8") as f:
            json.dump(epic, f, indent=2)
        logging.info(f"\n✅ All fields for {JIRA_EPIC_KEY} saved to {JIRA_EPIC_KEY}_fields.json")
