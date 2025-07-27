# custom_fields.py

# Define custom field IDs and their names (you can replace the IDs with actual custom field IDs from your Jira instance)
CUSTOM_FIELDS = {
    'customfield_10015': 'Start Date',
    'customfield_10058': 'End Date',
    'customfield_10001': 'Team',
    # Add more custom fields as needed
}

def get_custom_field_value(field_id, fields):
    """Fetch the value of a custom field based on the field ID."""
    return fields.get(field_id, 'Not available')

def get_custom_fields(fields):
    """Fetch all custom fields from a set of issue fields."""
    custom_field_values = {}
    
    for field_id, field_name in CUSTOM_FIELDS.items():
        value = get_custom_field_value(field_id, fields)
        custom_field_values[field_name] = value
    
    return custom_field_values

# Optionally, create a list of custom field names for easy reference
CUSTOM_FIELD_NAMES = list(CUSTOM_FIELDS.values())

