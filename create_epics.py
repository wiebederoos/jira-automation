import os
import json
import logging
import requests
from constants import CREATE_ISSUE_URL, EPICS_DIRECTORY, JIRA_PROJECT_KEY
from auth import jira_auth, HEADERS, AUTH
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_epic_data(file_path):
    """Load JSON data from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load {file_path}: {e}")
        return None

def create_epic(file_path):
    """Send POST request to create an Epic in Jira."""
    data = load_epic_data(file_path)
    if not data:
        return

    issue_payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "issuetype": {
                "name": "Epic"
            },
            **data
        }
    }

    try:
        response = requests.post(CREATE_ISSUE_URL, auth=AUTH, headers=HEADERS, json=issue_payload)
        if response.status_code == 201:
            issue_key = response.json().get("key")
            logging.info(f"Successfully created Epic {issue_key} from {file_path}")
        else:
            logging.error(f"Failed to create Epic from {file_path}: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception(f"Exception creating Epic from {file_path}: {e}")

def create_epics_for_project():
    epic_files = [os.path.join(EPICS_DIRECTORY, f) for f in os.listdir(EPICS_DIRECTORY) if f.endswith('.json')]

    if not epic_files:
        logging.warning("No epic files found to process.")
        return

    logging.info(f"Found {len(epic_files)} epic files to process.")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(create_epic, file): file for file in epic_files}

        for future in as_completed(futures):
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                logging.error(f"Unhandled error processing {file}: {e}")

if __name__ == "__main__":
    jira_auth()
    create_epics_for_project()
