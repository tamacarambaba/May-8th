import os
import json
from langdetect import detect, LangDetectException
from collections import defaultdict
from datetime import datetime

# Папки с данными
data_dirs = [
    r"D:\PS Data\PS 8 May (filtered by date)\de (09.05)", r"D:\PS Data\PS 8 May (filtered by date)\en (09.05)", r"D:\PS Data\PS 8 May (filtered by date)\ru (09.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\de (10.05)", r"D:\PS Data\PS 8 May (filtered by date)\en (10.05)", r"D:\PS Data\PS 8 May (filtered by date)\ru (10.05)"
]

# Словари: дата -> язык -> список id
date_language_map = {
    "2025-05-08": defaultdict(list),
    "2025-05-09": defaultdict(list)
}
date_total_count = {
    "2025-05-08": 0,
    "2025-05-09": 0
}

for folder in data_dirs:
    for filename in os.listdir(folder):
        if not filename.endswith("_metadata.json"):
            continue

        filepath = os.path.join(folder, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            meta = data.get("video_metadata", {})
            description = meta.get("description", "")
            video_id = str(meta.get("id"))
            time_created = meta.get("time_created", "")

            if not description or not video_id or not time_created:
                continue

            try:
                created_date = datetime.fromisoformat(time_created).date().isoformat()
                if created_date not in date_language_map:
                    continue
            except Exception:
                continue

            try:
                lang = detect(description)
            except LangDetectException:
                lang = "unknown"

            date_language_map[created_date][lang].append(video_id)
            date_total_count[created_date] += 1

        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"[!] Error processing file {filepath}: {e}")
            continue

# Сохраняем результаты
for date_str, lang_map in date_language_map.items():
    total = date_total_count[date_str]
    out_file = f"language_distribution_{date_str[-5:].replace('-', '-')}.txt"  # 08-05 or 09-05

    with open(out_file, 'w', encoding='utf-8') as f:
        for lang, ids in sorted(lang_map.items(), key=lambda x: len(x[1]), reverse=True):
            percentage = (len(ids) / total) * 100 if total > 0 else 0
            f.write(f"{lang}: {len(ids)} ({percentage:.2f}%)\n")

    print(f"[✓] Language distribution for {date_str} saved to {out_file}")
