import requests
from auth import get_jira_auth  # Assumed you have an authentication function
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def fetch_all_custom_fields():
    """Fetch all fields and distinguish between system and admin-created custom fields."""
    try:
        auth, domain = get_jira_auth()  # Fetch Jira authentication from your auth module
    except ValueError as e:
        print(f"❌ Authentication failed: {e}")
        return []

    url = f"https://{domain}.atlassian.net/rest/api/3/field"

    headers = {
        "Accept": "application/json"
    }

    # Pagination parameters
    start_at = 0
    max_results = 100  # Number of fields per page (max 1000)

    system_fields = []
    admin_custom_fields = []

    while True:
        # Add pagination parameters to the request
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }

        # Send the GET request
        response = requests.get(url, headers=headers, auth=auth, params=params)

        if response.status_code == 200:
            fields_data = response.json()

            # Filter fields into system fields and admin-created custom fields
            for field in fields_data:
                # Check if the field is a custom field
                if field.get('custom', False):
                    admin_custom_fields.append(field)
                else:
                    # Assuming system fields have the 'id' field like 'assignee' or 'priority'
                    system_fields.append(field)

            # If there are fewer results than maxResults, we've reached the last page
            if len(fields_data) < max_results:
                break

            # Move to the next page
            start_at += max_results
        else:
            print(f"❌ Failed to fetch fields. Status Code: {response.status_code}")
            print(response.text)
            break

    # Sort fields alphabetically by 'name'
    system_fields.sort(key=lambda x: x.get('name', '').lower())
    admin_custom_fields.sort(key=lambda x: x.get('name', '').lower())

    print(f"Found {len(system_fields)} system fields and {len(admin_custom_fields)} admin-created custom fields:")

    # Print system fields
    print("\n--- System Fields ---")
    for field in system_fields:
        field_id = field.get('id', 'No ID available')
        field_name = field.get('name', 'No name available')
        print(f"ID: {field_id} - Name: {field_name}")

    # Print admin-created custom fields
    print("\n--- Admin-Created Custom Fields ---")
    for field in admin_custom_fields:
        field_id = field.get('id', 'No ID available')
        field_name = field.get('name', 'No name available')
        print(f"ID: {field_id} - Name: {field_name}")

    return system_fields, admin_custom_fields

# Example usage:
fetch_all_custom_fields()
