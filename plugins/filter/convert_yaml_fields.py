# filter_plugins/yaml_to_dict.py

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
