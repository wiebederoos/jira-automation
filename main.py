# main.py
import os
import requests
import logging
from auth import get_jira_auth
from logging_config import configure_logging

# Configure logging
configure_logging()

JIRA_DOMAIN=os.getenv('JIRA_DOMAIN')

def main():
    try:
        auth, domain = get_jira_auth()
    except ValueError as e:
        logging.error(f"Authentication failed: {e}")
        print(f"❌ Error: {e}")
        return

    url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/myself"
    headers = {"Accept": "application/json"}

    logging.info(f"Sending request to {url} for authentication.")

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200:
        data = response.json()
        account_id = data.get("accountId")
        email_address = data.get("emailAddress")

        logging.info(f"Successfully authenticated. Account ID: {account_id}")
        print("✅ Authenticated successfully.")
        print(f"Account ID: {account_id}")
        if email_address:
            print(f"Email Address: {email_address}")
        else:
            print("⚠️ Email address not available (restricted by Jira settings).")
    else:
        logging.error(f"Authentication failed. Status Code: {response.status_code}")
        print("❌ Authentication failed.")
        print(f"Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
