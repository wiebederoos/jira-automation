import requests
from auth import get_jira_auth  # Assumed you have an authentication function
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def fetch_epics_for_project(project_key):
    """Fetch all Epics for a specific project, including labels and custom fields."""
    try:
        auth, domain = get_jira_auth()  # Fetch Jira authentication from your auth module
    except ValueError as e:
        print(f"❌ Authentication failed: {e}")
        return

    url = f"https://{domain}.atlassian.net/rest/api/3/search"

    # Define the JQL query to fetch all Epics for a specific project
    jql_query = f'project = "{project_key}" AND issuetype = "Epic"'

    # Fields to include in the response (labels, custom fields, and any other fields you need)
    fields = "labels,customfield_10015,customfield_10058"  # Example custom fields (change as needed)

    # Request parameters
    params = {
        "jql": jql_query,
        "fields": fields,
        "maxResults": 1000  # Adjust if you expect more than 1000 results
    }

    headers = {
        "Accept": "application/json"
    }

    # Send the GET request
    response = requests.get(url, headers=headers, auth=auth, params=params)

    if response.status_code == 200:
        issues_data = response.json()

        # Loop through issues (Epics) and extract labels and custom fields
        for issue in issues_data['issues']:
            epic_key = issue['key']
            epic_fields = issue['fields']
            
            # Get labels
            labels = epic_fields.get('labels', [])

            # Get custom fields (adjust field names/IDs based on your Jira instance)
            custom_field_1 = epic_fields.get('customfield_10015', 'Not available')  # Replace with actual custom field ID
            custom_field_2 = epic_fields.get('customfield_10058', 'Not available')  # Replace with actual custom field ID

            # Print details for each Epic
            print(f"Epic Key: {epic_key}")
            print(f"Labels: {', '.join(labels) if labels else 'No labels assigned'}")
            print(f"Custom Field 1: {custom_field_1}")
            print(f"Custom Field 2: {custom_field_2}")
            print("-" * 50)

    else:
        print(f"❌ Failed to fetch Epics. Status Code: {response.status_code}")
        print(response.text)

# Example usage:
project_key = "ECS"  # Replace with your project key
fetch_epics_for_project(project_key)
