# field_config.py

# Fields to be fetched from Jira (custom fields and standard fields)
FIELDS_TO_FETCH_INTERNAL = [
    "labels"              # Standard field: labels
]

FIELDS_TO_FETCH_EXTERNAL = [
    "labels",              # Standard field: labels
    "customfield_10015",   # Start date
    "customfield_10058",   # End Date
    "customfield_10001",   # Teams
    "customfield_10059"    # Fix version 
]

FIELDS_TO_FETCH=FIELDS_TO_FETCH_EXTERNAL