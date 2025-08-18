import os
import requests
import logging
from dotenv import load_dotenv
from auth import get_jira_auth, HEADERS

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_DOMAIN=os.getenv('JIRA_DOMAIN')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')


auth = (JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json"
}

# API endpoint
url = f"{JIRA_BASE_URL}/rest/api/3/project/{JIRA_PROJECT_KEY}/versions"

# Load .env variables
load_dotenv()

def get_fix_versions():
    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()
        versions = response.json()
        logging.info(f"Found {len(versions)} fix versions in project '{JIRA_PROJECT_KEY}'.")
        for version in versions:
            print(f"- ID: {version.get('id')} | Name: {version.get('name')} | Released: {version.get('released')}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch fix versions: {e}")

if __name__ == "__main__":
    get_fix_versions()
