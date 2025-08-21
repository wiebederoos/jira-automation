# auth.py
import os
import logging
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from logging_config import configure_logging

# Load environment variables from .env
load_dotenv()

# Configure logging
configure_logging()

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")   

JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')

AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def jira_auth():
    try:
        if not all([JIRA_EMAIL, JIRA_API_TOKEN, JIRA_DOMAIN]):
            logging.error("Missing one or more required environment variables (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_DOMAIN).")
            raise ValueError("Missing JIRA_EMAIL, JIRA_API_TOKEN, or JIRA_DOMAIN in environment variables.")

        logging.info(f"Attempting authentication for {JIRA_EMAIL} with domain {JIRA_DOMAIN}.")
        HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    except ValueError as e:
        logging.error(f"❌ Authentication failed: {e}")
        return