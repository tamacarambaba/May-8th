import json
from src.helpers.path_helpers import *



# GET THE Value by filename and by key
def get_json_value_by_filename_and_key(base_path:str, json_file_name:str, key:str):
    json_file_path = join_paths(join_paths(base_path, "data\\helper_json_files"), json_file_name)
    return get_json_value_by_filepath_and_key(json_file_path, key)

# GET THE Value by filepath and key
def get_json_value_by_filepath_and_key(json_file_path:str, key:str):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(key)

# ADDS VALUE TO KEY OF JSON FILE   
def add_value_to_json_file(json_file_path:str, key:str, value):
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"File not found: {json_file_path}")

    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update or add the key-value pair
    data[key] = value

    # Write the updated data back to the file
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)