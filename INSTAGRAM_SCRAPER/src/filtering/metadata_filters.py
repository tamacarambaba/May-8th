from pathlib import Path
from typing import List, Union, Any
from src.helpers.dir_helpers import *
from src.helpers.path_helpers import *
from src.helpers.json_helpers import *

def get_caption_list(base_path, target_folder_path, json_dict_key:str = "caption"):
    """
    Walk through post folders inside `target_folder_path` and collect values for `json_dict_key`
    from each `metadata_<post_id>.json`.

    Folder structure (per post):
        <target_folder_path>/<post_id>/
            metadata_<post_id>.json

    Args:
        target_folder_path: Base folder that contains one subfolder per post (named by post_id).
        json_dict_key:      Key to look up in each metadata JSON.

    Returns:
        caption_list: list[str] with non-empty values returned by
                      get_json_value_by_filepath_and_key for each post.
                      If the helper returns a list, all non-empty strings inside are appended.
    """
    base = Path(join_paths(base_path, target_folder_path))
    caption_list = []

    if not base.exists() or not base.is_dir():
        return caption_list

    # Iterate only directories (post folders). Sort for deterministic order.
    for post_dir in base.iterdir():
        post_id = post_dir.name
        meta_path = Path(join_paths(post_dir, f"metadata_{post_id}.json"))
        if not meta_path.exists():
            continue

        try:
            value = get_json_value_by_filepath_and_key(str(meta_path), json_dict_key)
        except Exception:
            # Ignore files that can't be read/parsed; continue with others
            continue

        if isinstance(value, str):
            val = value.strip()
            if val:
                caption_list.append(val)

    return caption_list


def get_caption_hashtag_list(base_path, target_folder_path, json_dict_key: str = "caption_hashtags") -> List[List[str]]:
    """
    Walk through post folders inside `target_folder_path` and collect hashtag lists for `json_dict_key`
    from each `metadata_<post_id>.json`.

    Folder structure (per post):
        <target_folder_path>/<post_id>/
            metadata_<post_id>.json

    Args:
        base_path:          Base path for the scraper project.
        target_folder_path: Folder containing one subfolder per post (named by post_id).
        json_dict_key:      Key to look up in each metadata JSON (default: 'caption_hashtags').

    Returns:
        caption_hashtag_list: list[list[str]] with non-empty hashtag lists from each post.
    """
    base = Path(join_paths(base_path, target_folder_path))
    caption_hashtag_list = []

    if not base.exists() or not base.is_dir():
        return caption_hashtag_list

    # Iterate only directories (post folders)
    for post_dir in base.iterdir():
        post_id = post_dir.name
        meta_path = Path(join_paths(post_dir, f"metadata_{post_id}.json"))
        if not meta_path.exists():
            continue

        try:
            value = get_json_value_by_filepath_and_key(str(meta_path), json_dict_key)
        except Exception:
            continue  # Ignore files that can't be read/parsed

        if isinstance(value, list):
            hashtags = [tag.strip() for tag in value if isinstance(tag, str) and tag.strip()]
            if hashtags:  # only append non-empty hashtag lists
                caption_hashtag_list.append(hashtags)

    return caption_hashtag_list
