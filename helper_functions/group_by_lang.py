import os
import json
from langdetect import detect, LangDetectException
from collections import defaultdict

data_dirs = [
    r"D:\PS Data\PS 8 May (filtered by date)\de (09.05)", r"D:\PS Data\PS 8 May (filtered by date)\en (09.05)", r"D:\PS Data\PS 8 May (filtered by date)\ru (09.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\de (10.05)", r"D:\PS Data\PS 8 May (filtered by date)\en (10.05)", r"D:\PS Data\PS 8 May (filtered by date)\ru (10.05)"
]

language_id_map = defaultdict(list)
total_count = 0

for folder in data_dirs:
    for filename in os.listdir(folder):
        if not filename.endswith("_metadata.json"):
            continue

        filepath = os.path.join(folder, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            description = data.get("video_metadata", {}).get("description", "")
            video_id = str(data.get("video_metadata", {}).get("id"))

            if not description or not video_id:
                continue

            try:
                lang = detect(description)
            except LangDetectException:
                lang = "unknown"

            language_id_map[lang].append(video_id)
            total_count += 1

        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"[!] Ошибка при обработке файла {filepath}: {e}")
            continue

# Сохраняем списки id в отдельные файлы
for lang, ids in language_id_map.items():
    filename = f"ids_{lang}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for id_ in ids:
            f.write(id_ + '\n')

# Вывод долей языков
print("\n📊 Распределение языков:")
for lang, ids in sorted(language_id_map.items(), key=lambda x: len(x[1]), reverse=True):
    percentage = (len(ids) / total_count) * 100 if total_count > 0 else 0
    print(f"{lang}: {len(ids)} файлов ({percentage:.2f}%)")
