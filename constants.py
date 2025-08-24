import os
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

EPICS_DIRECTORY="epics"
LOG_FILE="jira_automation.log"

GET_ISSUE_URL = f"{JIRA_BASE_URL}/rest/api/3/search"
GET_FIELDS_URL = f"{JIRA_BASE_URL}/rest/api/3/field"
GET_TEAMS_URL = f"{JIRA_BASE_URL}/rest/teams/1.0/teams"
CREATE_ISSUE_URL = f"{JIRA_BASE_URL}/rest/api/3/issue"
CREATE_VERSION_URL = f"{JIRA_BASE_URL}/rest/api/3/version"
PROJECT_VERSIONS_URL = f"{JIRA_BASE_URL}/rest/api/3/project/{JIRA_PROJECT_KEY}/versions"
PROJECT_ISSUE_TYPES_FIELDS = f"{JIRA_BASE_URL}/rest/api/3/issue/createmeta?projectKeys={JIRA_PROJECT_KEY}&expand=projects.issuetypes.fields"
