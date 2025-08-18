import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Jira credentials and project
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Auth and headers
auth = (JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# API endpoint
create_version_url = f"{JIRA_BASE_URL}/rest/api/3/version"

def create_fix_version(name, description=None, release_date=None, released=False):
    payload = {
        "name": name,
        "project": JIRA_PROJECT_KEY,
        "released": released
    }

    if description:
        payload["description"] = description
    if release_date:
        payload["releaseDate"] = release_date  # Format: "YYYY-MM-DD"

    try:
        response = requests.post(create_version_url, auth=auth, headers=headers, json=payload)
        response.raise_for_status()
        version = response.json()
        logging.info(f"Fix Version created: {version.get('name')} (ID: {version.get('id')})")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create Fix Version: {e}")
        if e.response is not None:
            logging.error(f"Response: {e.response.status_code} - {e.response.text}")

if __name__ == "__main__":
    
    create_fix_version(
        name="Version X",
        description="Version X",
        release_date="2025-11-11",
        released=True
    )
