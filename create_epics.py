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

def find_epic_by_summary(summary):
    """Search for an Epic by summary in Jira."""
    jql = f'project="{JIRA_PROJECT_KEY}" AND issuetype=Epic AND summary~"{summary}"'
    search_url = f"{CREATE_ISSUE_URL.rsplit('/issue', 1)[0]}/search"
    params = {"jql": jql, "fields": "key,summary"}
    try:
        response = requests.get(search_url, auth=AUTH, headers=HEADERS, params=params)
        if response.status_code == 200:
            issues = response.json().get("issues", [])
            for issue in issues:
                if issue["fields"]["summary"].strip().lower() == summary.strip().lower():
                    return issue["key"]
        else:
            logging.error(f"Failed to search for Epic: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception(f"Exception searching for Epic: {e}")
    return None

def update_epic(issue_key, data):
    """Update an existing Epic in Jira."""
    update_url = f"{CREATE_ISSUE_URL}/{issue_key}"
    issue_payload = {"fields": data}
    try:
        response = requests.put(update_url, auth=AUTH, headers=HEADERS, json=issue_payload)
        if response.status_code == 204:
            logging.info(f"Successfully updated Epic {issue_key}")
        else:
            logging.error(f"Failed to update Epic {issue_key}: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception(f"Exception updating Epic {issue_key}: {e}")

def create_or_update_epic(file_path):
    """Create or update an Epic in Jira based on summary."""
    data = load_epic_data(file_path)
    if not data or "summary" not in data:
        logging.error(f"Missing summary in {file_path}")
        return

    summary = data["summary"]
    existing_key = find_epic_by_summary(summary)

    if existing_key:
        logging.info(f"Epic with summary '{summary}' exists as {existing_key}. Updating...")
        update_epic(existing_key, data)
    else:
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
        futures = {executor.submit(create_or_update_epic, file): file for file in epic_files}

        for future in as_completed(futures):
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                logging.error(f"Unhandled error processing {file}: {e}")

if __name__ == "__main__":
    jira_auth()
    create_epics_for_project()
