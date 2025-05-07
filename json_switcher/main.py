import json
from datetime import datetime as dt

today = dt.now().strftime('%Y%m%d')

# Set import paths.
config_original_PATH = fr""
data_original_PATH = fr""

# Set output paths.
config_updated_PATH = fr""
data_updated_PATH = fr""

def replace_values(obj, replacements):
    """
    Searches and replaces values in a dictionary or list.
    """
    if isinstance(obj, dict):
        return {k: replace_values(v, replacements) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_values(item, replacements) for item in obj]
    elif isinstance(obj, str):
        for old, new in replacements.items():
            obj = obj.replace(old, new)
        return obj
    else:
        return obj

in_json_files = [config_original_PATH, data_original_PATH]
out_json_files = [config_updated_PATH, data_updated_PATH]


for in_file, out_file in zip(in_json_files, out_json_files):
    with open(in_file, 'r', encoding="utf-8-sig") as file:
        config_data = json.load(file)

    replacements = {
      "original_value": "updated_value"
    } # in this dictionary, store the original value as the key and the updated value as the value.

    updated_config = replace_values(config_data, replacements)

    with open(out_file, 'w', encoding='utf-8') as file:
        json.dump(updated_config, file, indent=4)
    print(f'{file} updated successfully.')
