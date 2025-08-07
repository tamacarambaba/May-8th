import os
import json
from datetime import datetime, date

# Directories with metadata and videos
data_dirs = [
    r"D:\PS Data\PS 8 May (filtered by date)\de (09.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\de (10.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\en (09.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\en (10.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\ru (09.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\ru (10.05)"
]

# List of irrelevant hashtags (lowercase)
irrelevant_hashtags = {
    "fyp", "pourtoi", "algerie", "рекомендации"
}

deleted_files = 0
kept_files = 0

for dir_path in data_dirs:
    for filename in os.listdir(dir_path):
        if not filename.endswith("_metadata.json"):
            continue

        metadata_path = os.path.join(dir_path, filename)

        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            video_meta = data.get("video_metadata", {})
            hashtags = video_meta.get("hashtags", [])

            # Check hashtags — if all are irrelevant, delete the file
            for tag in hashtags:
                if tag.lower() in irrelevant_hashtags:
                    raise ValueError(f"Irrelevant hashtag found: {tag}")

            kept_files += 1

        except Exception as e:
            # Get id from filename
            file_id = filename.split("_")[1]
            json_to_delete = metadata_path
            video_to_delete = os.path.join(
                dir_path, filename.replace("_metadata.json", "_video.mp4"))

            # Delete files
            if os.path.exists(json_to_delete):
                os.remove(json_to_delete)
            if os.path.exists(video_to_delete):
                os.remove(video_to_delete)

            deleted_files += 1
            print(f"Deleted: {filename} — reason: {e}")

print(f"\nDone. Files kept: {kept_files}, deleted: {deleted_files}")
