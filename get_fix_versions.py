import os
import requests
import logging
from dotenv import load_dotenv
from auth import jira_auth, JIRA_BASE_URL, HEADERS, AUTH, JIRA_PROJECT_KEY 

# API endpoint
url = f"{JIRA_BASE_URL}/rest/api/3/project/{JIRA_PROJECT_KEY}/versions"

# Load .env variables
load_dotenv()

def get_fix_versions():
    try:
        response = requests.get(url, headers=HEADERS, auth=AUTH)
        response.raise_for_status()
        versions = response.json()
        logging.info(f"Found {len(versions)} fix versions in project '{JIRA_PROJECT_KEY}'.")
        for version in versions:
            logging.info(f"- ID: {version.get('id')} | Name: {version.get('name')} | Released: {version.get('released')}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch fix versions: {e}")

if __name__ == "__main__":
    get_fix_versions()
