import os
import requests
import logging
from auth import jira_auth, HEADERS, AUTH
from constants import GET_TEAMS_URL

def fetch_all_teams():
    
    start_at = 0
    max_results = 50
    all_teams = []

    while True:
        params = {"startAt": start_at, "maxResults": max_results}
        logging.info(f"Fetching teams starting at {start_at}")
        
        try:
            response = requests.get(GET_TEAMS_URL, headers=HEADERS, auth=AUTH, params=params)
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
        logging.info(f"ID: {team.get('id')} | Name: {team.get('name')} | Type: {team.get('type')} | Members: {team.get('memberCount')}")
    
    return all_teams

if __name__ == "__main__":
    jira_auth()
    fetch_all_teams()
