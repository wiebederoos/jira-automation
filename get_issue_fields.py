import os
import requests
import logging
from auth import jira_auth, HEADERS, AUTH
from constants import PROJECT_ISSUE_TYPES_FIELDS

def list_fields_per_issue_type():
    response = requests.get(PROJECT_ISSUE_TYPES_FIELDS, headers=HEADERS, auth=AUTH)
    if response.status_code != 200:
        logging.error(f"Error: {response.status_code} - {response.text}")
        return

    data = response.json()
    project = data.get("projects", [])[0]
    issue_types = project.get("issuetypes", [])

    for issue_type in issue_types:
        logging.info(f"\n📌 Issue Type: {issue_type['name']}")
        fields = issue_type.get("fields", {})
        for field_id, field_info in fields.items():
            field_name = field_info.get("name")
            required = field_info.get("required", False)
            logging.info(f"   - {field_name} (ID: {field_id}){' [REQUIRED]' if required else ''}")

if __name__ == "__main__":
    jira_auth()
    list_fields_per_issue_type()