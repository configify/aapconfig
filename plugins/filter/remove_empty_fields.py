# filter_plugins/remove_empty_fields.py

def remove_empty_fields(data, fields):
    """
    Removes specified fields from a list of dictionaries if they have empty values.

    Args:
        data (list): List of dictionaries.
        fields (list): List of fields to remove if they are empty.

    Returns:
        list: Updated list of dictionaries with specified empty fields removed.
    """
    def is_empty(value):
        """Returns True if the value is empty (None, '', [], {}, etc.)"""
        return value in [None, '', [], {}, False]

    for item in data:
        for field in fields:
            if field in item and is_empty(item[field]):
                del item[field]
    return data

class FilterModule(object):
    def filters(self):
        return {
            'remove_empty_fields': remove_empty_fields
        }
