# field_mappings.py

# Custom field mappings (Field ID -> Field Name)
CUSTOM_FIELDS_INTERNAL = {
}

CUSTOM_FIELDS_EXTERNAL = {
    'customfield_10015': 'Start date',
    'customfield_10058': 'End date',
    'customfield_10001': 'Team',
    'customfield_10059': 'Fix version',
    'priority': 'priority',
    'project': 'project'
}

CUSTOM_FIELDS=CUSTOM_FIELDS_EXTERNAL

def get_custom_field_value(field_id, fields):
    """Fetch the value of a custom field based on the field ID."""
    return fields.get(field_id, 'Not available')

def fetch_custom_fields(fields):    
    """Fetch all custom fields from a set of issue fields."""
    custom_field_values = {}
    
    for field_id, field_name in CUSTOM_FIELDS.items():
        #print(field_id)
        value = get_custom_field_value(field_id, fields)
        custom_field_values[field_name] = value
    
    return custom_field_values