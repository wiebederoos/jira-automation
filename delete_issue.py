import requests
import logging
from constants import JIRA_BASE_URL
from auth import jira_auth, HEADERS, AUTH

def delete_issue(issue_key):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    response = requests.delete(url, headers=HEADERS, auth=AUTH)
    if response.status_code == 204:
        logging.info(f"✅ Issue {issue_key} deleted successfully")
    else:
        logging.info(f"❌ Failed to delete {issue_key}: {response.status_code} - {response.text}")

if __name__ == "__main__":    
    issue_key = input("Enter the Jira issue key to delete: ").strip()
    jira_auth()
    delete_issue(issue_key)

