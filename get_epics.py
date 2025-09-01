import requests
import logging
from auth import jira_auth, HEADERS, AUTH
from constants import GET_ISSUE_URL, JIRA_PROJECT_KEY
from field_config import FIELDS_TO_FETCH
from custom_field_mappings import fetch_custom_fields

def fetch_epics_for_project(project_key):
    """Fetch all Epics for a specific project, including summary, priority, labels, custom fields, team name and team ID."""

    # Define the JQL query to fetch all Epics for a specific project
    jql_query = f'project = "{project_key}" AND issuetype = "Epic"'

    # Use the fields from field_config.py (FLEXIBLE: Add or remove fields as needed)
    fields = ",".join(FIELDS_TO_FETCH)

    # Request parameters
    params = {
        "jql": jql_query,
        "fields": fields,
        "maxResults": 1000  # Adjust if you expect more than 1000 results
    }

    # Send the GET request
    response = requests.get(GET_ISSUE_URL, headers=HEADERS, auth=AUTH, params=params)

    if response.status_code == 200:
        issues_data = response.json()

        # Loop through issues (Epics) and extract summary, priority, labels and custom fields
        for issue in issues_data['issues']:
            epic_key = issue['key']
            epic_fields = issue['fields']
            epic_summary = epic_fields.get('summary', 'No summary')
            labels = epic_fields.get('labels', [])
            epic_priority = epic_fields.get('priority', {}).get('name', 'No priority')  # <-- Added priority extraction
            project = epic_fields.get('project', {}).get('project', 'No project')  # <-- Added project extraction
            


            # Get custom fields using the updated custom_fields.py logic
            custom_field_values = fetch_custom_fields(epic_fields)

            # Extract team name and team id if present
            team_name = custom_field_values.get("team", "N/A")
            team_id = custom_field_values.get("Team ID", "N/A")

            # Print details for each Epic
            logging.info(f"Epic Priority: {epic_priority}")  # <-- Added to output
            logging.info(f"Epic Key: {epic_key}")
            logging.info(f"Epic Summary: {epic_summary}")
            logging.info(f"Labels: {', '.join(labels) if labels else 'No labels assigned'}")
            logging.info(f"Project: {project}")
            logging.info(f"Team Name: {team_name}")
            logging.info(f"Team ID: {team_id}")
            for field_name, field_value in custom_field_values.items():
                if field_name not in ["Team Name", "Team ID"]:
                    logging.info(f"{field_name}: {field_value}")
            logging.info("-" * 50)

    else:
        logging.error(f"❌ Failed to fetch Epics. Status Code: {response.status_code}")
        logging.error(response.text)

if __name__ == "__main__":
    jira_auth()
    fetch_epics_for_project(JIRA_PROJECT_KEY)



