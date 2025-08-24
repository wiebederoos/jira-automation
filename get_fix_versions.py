import requests
import logging
from auth import jira_auth, HEADERS, AUTH
from constants import JIRA_PROJECT_KEY, PROJECT_VERSIONS_URL

def get_fix_versions():
    try:
        response = requests.get(PROJECT_VERSIONS_URL, headers=HEADERS, auth=AUTH)
        response.raise_for_status()
        versions = response.json()
        logging.info(f"Found {len(versions)} fix versions in project '{JIRA_PROJECT_KEY}'.")
        for version in versions:
            logging.info(f"- ID: {version.get('id')} | Name: {version.get('name')} | Released: {version.get('released')}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch fix versions: {e}")

if __name__ == "__main__":
    jira_auth()
    get_fix_versions()
