import requests
from auth import jira_auth, JIRA_BASE_URL, HEADERS, AUTH, JIRA_PROJECT_KEY  # Assumed you have an authentication function
from dotenv import load_dotenv
import logging
import logging.config
import os
from field_config import FIELDS_TO_FETCH  # Import the fields list from field_config.py
from custom_field_mappings import fetch_custom_fields  # Import custom field fetcher
from logging_config import configure_logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
configure_logging()

GET_ISSUE_URL = f"{JIRA_BASE_URL}/rest/api/3/search"

def fetch_epics_for_project(project_key):
    """Fetch all Epics for a specific project, including labels and custom fields."""

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

        # Loop through issues (Epics) and extract labels and custom fields
        for issue in issues_data['issues']:
            epic_key = issue['key']
            epic_fields = issue['fields']
            
            # Get labels
            labels = epic_fields.get('labels', [])

            # Get custom fields using the updated custom_fields.py logic
            custom_field_values = fetch_custom_fields(epic_fields)            

            # Print details for each Epic
            logging.info(f"Epic Key: {epic_key}")
            logging.info(f"Labels: {', '.join(labels) if labels else 'No labels assigned'}")
            for field_name, field_value in custom_field_values.items():
                logging.info(f"{field_name}: {field_value}")
            logging.info("-" * 50)

    else:
        logging.error(f"❌ Failed to fetch Epics. Status Code: {response.status_code}")
        logging.error(response.text)

if __name__ == "__main__":
    jira_auth()
    fetch_epics_for_project(JIRA_PROJECT_KEY)


