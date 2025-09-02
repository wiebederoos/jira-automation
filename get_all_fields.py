import requests
import logging
from constants import GET_FIELDS_URL, PROJECT_ISSUE_TYPES_FIELDS
from auth import jira_auth, HEADERS, AUTH

def fetch_system_fields():
    """Fetch all system fields from Jira."""
    response = requests.get(GET_FIELDS_URL, headers=HEADERS, auth=AUTH)
    if response.status_code == 200:
        fields = response.json()
        logging.info(f"Fetched {len(fields)} system fields.")
        return fields
    else:
        logging.error(f"Failed to fetch system fields: {response.status_code} - {response.text}")
        return None

def fetch_project_fields():
    """Fetch all project-specific fields from Jira."""
    response = requests.get(PROJECT_ISSUE_TYPES_FIELDS, headers=HEADERS, auth=AUTH)
    if response.status_code == 200:
        data = response.json()
        logging.info("Fetched project-specific fields.")
        return data
    else:
        logging.error(f"Failed to fetch project fields: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    jira_auth()
    system_fields = fetch_system_fields()
    project_fields = fetch_project_fields()
    logging.info("System Fields:", system_fields)
    logging.info("Project Fields:", project_fields)