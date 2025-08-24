import os
import requests
import logging
from dotenv import load_dotenv
from constants import CREATE_VERSION_URL, JIRA_PROJECT_KEY
from auth import jira_auth, HEADERS, AUTH

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
        response = requests.post(CREATE_VERSION_URL, auth=AUTH, headers=HEADERS, json=payload)
        response.raise_for_status()
        version = response.json()
        logging.info(f"Fix Version created: {version.get('name')} (ID: {version.get('id')})")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create Fix Version: {e}")
        if e.response is not None:
            logging.error(f"Response: {e.response.status_code} - {e.response.text}")

if __name__ == "__main__":
    jira_auth()
    create_fix_version(
        name="Version Y",
        description="Version Y",
        release_date="2025-11-11",
        released=True
    )
