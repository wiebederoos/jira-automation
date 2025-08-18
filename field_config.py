# field_config.py

# Fields to be fetched from Jira (custom fields and standard fields)
FIELDS_TO_FETCH = [
    "labels",              # Standard field: labels
    "customfield_10015",   # Start date
    "customfield_10058",   # End Date
    "customfield_10001",   # Teams
    "customfield_10059"    # Fix version 
    # Add more custom fields here as needed
]