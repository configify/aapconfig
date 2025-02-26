DOCUMENTATION = r"""
name: convert_yaml_fields
short_description: A filter that converts specified dictionary fields in provided list of dictionaries to json
description:
  - Returns list of dictionaries with modified fields
  - Fields are converted from a string (in yaml format) to a dictionary (json)
options:
  _data:
    description: A list of dictionaries
    type: list
    elements: dictionaries
    required: true
  _fields:
    description: Dictionary fields to convert
    type: str
    required: true
"""

EXAMPLES = r'''
- name: Convert extra variables to dict
  ansible.builtin.set_fact:
    converted_list_of_dict: "{{ list_of_dict | configify.aapconfig.convert_yaml_fields(fields=['extra_vars']) }}"
'''

import yaml

def convert_yaml_fields(data, fields):
    """
    Convert specified YAML fields to dictionaries.
    
    Args:
        data (list): List of dictionaries containing YAML strings.
        fields (list): List of fields to convert from YAML string to dictionary.

    Returns:
        list: Data with the specified fields converted to dictionaries.
    """
    for item in data:
        for field in fields:
            if field in item:
                if not item[field] or item[field] == '---':
                    item[field] = {}
                else:
                    try:
                        item[field] = yaml.safe_load(item[field])
                    except yaml.YAMLError as e:
                        raise ValueError(f"Error converting field '{field}': {e}")
    return data

class FilterModule(object):
    def filters(self):
        return {
            'convert_yaml_fields': convert_yaml_fields
        }
