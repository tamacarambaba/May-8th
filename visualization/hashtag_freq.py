import os
import json
from collections import Counter
import matplotlib.pyplot as plt

# Путь к файлу с ID (один ID на строку)
id_file = r"D:\PS Data\Language groups (new)\ids_ru.txt"

# Папки, где лежат метаданные
metadata_dirs = [
    r"D:\PS Data\PS 8 May (filtered by date)\ru (09.05)",
    r"D:\PS Data\PS 8 May (filtered by date)\ru (10.05)",
]

# Загрузка ID
with open(id_file, "r", encoding="utf-8") as f:
    valid_ids = set(line.strip() for line in f if line.strip())

# Сбор хэштегов
hashtag_counter = Counter()

for directory in metadata_dirs:
    if not os.path.exists(directory):
        print(f"Папка не найдена: {directory}")
        continue

    for filename in os.listdir(directory):
        if not filename.endswith("_metadata.json"):
            continue

        try:
            file_id = filename.split("_")[1]
        except IndexError:
            continue

        if file_id not in valid_ids:
            continue

        file_path = os.path.join(directory, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                hashtags = data.get("video_metadata", {}).get("hashtags", [])
                hashtag_counter.update(hashtags)
        except Exception as e:
            print(f"Ошибка при чтении {file_path}: {e}")

# Топ-5 хэштегов
top_hashtags = hashtag_counter.most_common(5)

# Визуализация
labels, counts = zip(*top_hashtags)
plt.figure(figsize=(10, 6))
plt.bar(labels, counts, color='skyblue')
plt.title("Top 5 Hashtags")
plt.ylabel("Frequency")
plt.xlabel("Hashtag")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
