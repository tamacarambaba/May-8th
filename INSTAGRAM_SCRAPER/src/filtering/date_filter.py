from datetime import date, datetime
import json
from pathlib import Path
import shutil
from typing import List, Union


def get_posts_by_date(
    target_date,
    target_folder_path,
    output_folder_path,
    metadata_key: str = "post_datetime"
):
    """
    Copy all post folders whose metadata `<metadata_key>` has the same Y-M-D as `target_date`.

    Folder structure per post (as you described):
        <target_folder_path>/<post_id>/
            metadata_<post_id>.json
            ... (media files)

    Args:
        target_date:       The date to match. Accepts 'YYYY-MM-DD', 'YYYY-MM-DD HH:MM:SS',
                           datetime, or date. Time part is ignored.
        target_folder_path: Folder containing post subfolders (named by post_id).
        output_folder_path: Destination folder where matching post folders will be copied.
        metadata_key:       JSON key with the post datetime (default: "post_datetime").

    Returns:
        A list of post_ids that were copied.
    """
    # --- normalize input paths ---
    src_root = Path(target_folder_path)
    dst_root = Path(output_folder_path)
    dst_root.mkdir(parents=True, exist_ok=True)

    # --- normalize target_date to a date() ---
    if isinstance(target_date, datetime):
        target_dt = target_date.date()
    elif isinstance(target_date, date):
        target_dt = target_date
    elif isinstance(target_date, str):
        s = target_date.strip()
        # Try common formats: 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD'
        try:
            target_dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S").date()
        except ValueError:
            target_dt = datetime.strptime(s, "%Y-%m-%d").date()
    else:
        raise TypeError("target_date must be str, datetime, or date")

    if not src_root.exists() or not src_root.is_dir():
        print(f"⚠ Source folder not found or not a directory: {src_root}")
        return []

    copied: List[str] = []

    # --- iterate post folders ---
    for post_dir in sorted((p for p in src_root.iterdir() if p.is_dir()), key=lambda p: p.name):
        post_id = post_dir.name
        meta_path = post_dir / f"metadata_{post_id}.json"
        if not meta_path.exists():
            # No metadata file -> skip
            continue

        # Read post_datetime from JSON
        try:
            with meta_path.open("r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            # Corrupt/invalid JSON -> skip
            continue

        raw_value = meta.get(metadata_key)
        if not raw_value or not isinstance(raw_value, str):
            continue

        # Parse metadata date string like "2025-01-22 00:00:00" (ignore time)
        try:
            # First try full timestamp
            post_dt = datetime.strptime(raw_value.strip(), "%Y-%m-%d %H:%M:%S").date()
        except ValueError:
            try:
                # Fallback to plain date
                post_dt = datetime.strptime(raw_value.strip(), "%Y-%m-%d").date()
            except ValueError:
                # Unrecognized date format -> skip this post
                continue

        # Compare only Y-M-D
        if post_dt == target_dt:
            dest_dir = dst_root / post_id
            # Copy entire post folder (overwrite/merge if it already exists)
            shutil.copytree(post_dir, dest_dir, dirs_exist_ok=True)
            copied.append(post_id)

    print(f"✅ Copied {len(copied)} post folder(s) for date {target_dt} to: {dst_root}")
    return copied