DOCUMENTATION = r"""
name: remove_empty_fields
short_description: A filter that removes specified fields if empty from each dictionary in a list of dictionaries
description:
  - Returns list of dictionaries without specified fields if they were empty
options:
  _data:
    description: A list of dictionaries
    type: list
    elements: dictionaries
    required: true
  _fields:
    description: Dictionary fields to remove
    type: str
    required: true
"""

EXAMPLES = r'''
- name: Remove empty variables from each dict
  ansible.builtin.set_fact:
    clean_list_of_dict: "{{ list_of_dict | configify.aapconfig.remove_empty_fields(fields=['field_that_is_often_empty']) }}"
'''


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
