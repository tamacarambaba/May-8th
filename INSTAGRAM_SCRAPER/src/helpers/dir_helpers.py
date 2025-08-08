import os
import json
from src.helpers.path_helpers import join_paths
from src.helpers.json_helpers import get_json_value_by_filename_and_key


# CREATES hashtag dir in posts if doesnt exists yet and returns true if it already existed
def create_hashtag_dir(base_path:str, hashtag_dir_name:str):
    new_dir_path    = join_paths(join_paths(base_path, get_json_value_by_filename_and_key(base_path, "dir_paths.json","posts_by_hashtags_path")), hashtag_dir_name)
    existed         = os.path.exists(new_dir_path)

    os.makedirs(new_dir_path, exist_ok=True)
    return not existed

# CREATES creates new post dir in the right hashtag dir if post dir doesnt exists yet, returns true, if it created a new folder
def create_post_dir(base_path:str, hashtag:str, post_id:str):
    post_dir_path   = join_paths(join_paths(join_paths(base_path, get_json_value_by_filename_and_key(base_path, "dir_paths.json","posts_by_hashtags_path")), hashtag), post_id)
    existed     = os.path.exists(post_dir_path)

    # CREATES new folder post folder and metadata file, only if it doesnt exist yet, returns true, if new folder was created
    if True != existed:
        os.makedirs(post_dir_path, exist_ok=True)
        create_metadata_file(base_path, post_dir_path, post_id)
    
    return not existed

# CREATES the metadata json file for the post dir and adds the structure aninitialized to the metadata json file
def create_metadata_file(base_path:str, post_dir_path:str, post_id:str):
    post_metadata_path = join_paths(post_dir_path, ("metadata_" + post_id + ".json"))
    metadata_structure = get_json_value_by_filename_and_key(base_path, "post_metadata_structure.json", "post_metadata_structure")

    with open(post_metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata_structure, f, indent=4)



