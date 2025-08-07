import os
import json

data_dirs = [
    r"D:\PS Data\PS 8 May (filtered by date)\de (09.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\en (09.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\ru (09.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\de (10.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\en (10.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\ru (10.05)"
]

hashtags_by_video = []

for folder in data_dirs:
    for filename in os.listdir(folder):
        if not filename.endswith("_metadata.json"):
            continue

        filepath = os.path.join(folder, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            hashtags = data.get("video_metadata", {}).get("hashtags", [])
            if hashtags and isinstance(hashtags, list):
                hashtags_by_video.append(hashtags)

        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"[!] Error reading {filepath}: {e}")

# Сохраняем результат в файл
with open("hashtags_by_video.txt", "w", encoding="utf-8") as f:
    for tag_list in hashtags_by_video:
        f.write(str(tag_list) + "\n")

print(f"[✓] Saved {len(hashtags_by_video)} hashtag groups to hashtags_by_video.txt")
