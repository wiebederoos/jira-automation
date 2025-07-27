# fields.py

# Custom field IDs and their names (Replace with actual field IDs and names from your Jira)
CUSTOM_FIELDS = {
    'customfield_10058': 'Start Date',
    'customfield_10015': 'End Date',
    'customfield_10002': 'Estimated Effort',
    'customfield_10003': 'Story Points',
    # Add more custom fields as needed
}

# Standard fields to query
STANDARD_FIELDS = [
    'labels',          # Labels of the issue
    'assignee',        # Assignee details
    'summary',         # Epic summary
    'created',         # Created date
    'updated',         # Last updated date
    'duedate'          # Due date
]

# Combine both custom and standard fields
ALL_FIELDS = list(CUSTOM_FIELDS.values()) + STANDARD_FIELDS

def get_all_fields():
    """Return a comma-separated list of all fields."""
    return ','.join(ALL_FIELDS)
