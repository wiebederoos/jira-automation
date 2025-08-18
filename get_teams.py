import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

if not all([JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
    raise ValueError("Missing required Jira environment variables.")

# Auth and headers
auth = (JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json"
}

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_all_teams():
    url = f"{JIRA_BASE_URL}/rest/teams/1.0/teams"
    start_at = 0
    max_results = 50
    all_teams = []

    while True:
        params = {"startAt": start_at, "maxResults": max_results}
        logging.debug(f"Fetching teams starting at {start_at}")
        
        try:
            response = requests.get(url, headers=headers, auth=auth, params=params)
            response.raise_for_status()
            data = response.json()

            teams = data.get("values", [])
            all_teams.extend(teams)

            if not data.get("isLast", True):
                start_at += max_results
            else:
                break

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch teams: {e}")
            break

    logging.info(f"Fetched {len(all_teams)} teams.")
    for team in all_teams:
        print(f"ID: {team.get('id')} | Name: {team.get('name')} | Type: {team.get('type')} | Members: {team.get('memberCount')}")
    
    return all_teams

if __name__ == "__main__":
    fetch_all_teams()
