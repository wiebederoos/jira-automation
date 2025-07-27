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

def get_jira_auth():
    """Returns Jira Basic Auth object and domain."""
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")
    domain = os.getenv("JIRA_DOMAIN")

    if not all([email, token, domain]):
        logging.error("Missing one or more required environment variables (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_DOMAIN).")
        raise ValueError("Missing JIRA_EMAIL, JIRA_API_TOKEN, or JIRA_DOMAIN in environment variables.")

    logging.info(f"Attempting authentication for {email} with domain {domain}.")
    auth = HTTPBasicAuth(email, token)
    return auth, domain
