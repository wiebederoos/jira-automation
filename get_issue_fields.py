import os
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

auth = (JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json"
}

def list_fields_per_issue_type():
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/createmeta?projectKeys={JIRA_PROJECT_KEY}&expand=projects.issuetypes.fields"

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return

    data = response.json()
    project = data.get("projects", [])[0]
    issue_types = project.get("issuetypes", [])

    for issue_type in issue_types:
        print(f"\n📌 Issue Type: {issue_type['name']}")
        fields = issue_type.get("fields", {})
        for field_id, field_info in fields.items():
            field_name = field_info.get("name")
            required = field_info.get("required", False)
            print(f"   - {field_name} (ID: {field_id}){' [REQUIRED]' if required else ''}")

if __name__ == "__main__":
    list_fields_per_issue_type()