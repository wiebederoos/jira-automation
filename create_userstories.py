import os
import json
import logging
import requests
from constants import CREATE_ISSUE_URL, USERSTORY_DIRECTORY, JIRA_PROJECT_KEY
from auth import jira_auth, HEADERS, AUTH
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_userstory_data(file_path):
    """Load JSON data from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load {file_path}: {e}")
        return None

def find_userstory_by_summary(summary):
    """Search for a Userstory by summary in Jira."""
    jql = f'project="{JIRA_PROJECT_KEY}" AND issuetype=Story AND summary~"{summary}"'
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
            logging.error(f"Failed to search for Story: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception(f"Exception searching for Story: {e}")
    return None

def update_userstory(issue_key, data):
    """Update an existing userstory in Jira."""
    update_url = f"{CREATE_ISSUE_URL}/{issue_key}"
    issue_payload = {"fields": data}
    try:
        response = requests.put(update_url, auth=AUTH, headers=HEADERS, json=issue_payload)
        if response.status_code == 204:
            logging.info(f"Successfully updated userstory {issue_key}")
        else:
            logging.error(f"Failed to update userstory {issue_key}: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception(f"Exception updating userstory {issue_key}: {e}")

def create_or_update_userstory(file_path):
    """Create or update a userstory in Jira based on summary."""
    data = load_userstory_data(file_path)
    # Validate that 'fields' exists and 'summary' is present inside 'fields'
    if not data or "fields" not in data or "summary" not in data["fields"]:
        logging.error(f"Missing 'fields' or 'summary' in {file_path}")
        return

    summary = data["fields"]["summary"]
    existing_key = find_userstory_by_summary(summary)

    if existing_key:
        logging.info(f"Story with summary '{summary}' exists as {existing_key}. Updating...")
        update_userstory(existing_key, data["fields"])
    else:
        issue_payload = {
            "fields": {
                "project": {
                    "key": JIRA_PROJECT_KEY
                },
                "issuetype": {
                    "name": "Story"
                },
                **{k: v for k, v in data["fields"].items() if k not in ["project", "issuetype"]}
            }
        }
        try:
            response = requests.post(CREATE_ISSUE_URL, auth=AUTH, headers=HEADERS, json=issue_payload)
            if response.status_code == 201:
                issue_key = response.json().get("key")
                logging.info(f"Successfully created userstory {issue_key} from {file_path}")
            else:
                logging.error(f"Failed to create userstory from {file_path}: {response.status_code} - {response.text}")
        except Exception as e:
            logging.exception(f"Exception creating userstory from {file_path}: {e}")

def create_userstory_for_project():
    Story_files = [os.path.join(USERSTORY_DIRECTORY, f) for f in os.listdir(USERSTORY_DIRECTORY) if f.endswith('.json')]

    if not Story_files:
        logging.warning("No userstory files found to process.")
        return

    logging.info(f"Found {len(Story_files)} userstory files to process.")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(create_or_update_userstory, file): file for file in Story_files}

        for future in as_completed(futures):
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                logging.error(f"Unhandled error processing {file}: {e}")

if __name__ == "__main__":
    jira_auth()
    create_userstory_for_project()
