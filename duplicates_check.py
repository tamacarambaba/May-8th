import os
import re
from collections import Counter

# Путь к основной папке
base_dir = "data"
languages = ["en", "de", "ru"]

# Регулярка для извлечения TikTok ID
id_pattern = re.compile(r"tiktok_(\d+)_")

# Для хранения статистики и всех уникальных ID
stats = {}
unique_ids = set()

for lang in languages:
    folder_path = os.path.join(base_dir, lang)
    all_ids = []

    if not os.path.exists(folder_path):
        print(f"⚠️ Папка '{lang}' не найдена, пропускаем.")
        continue

    # Проходим по всем файлам в текущей языковой папке
    for root, _, files in os.walk(folder_path):
        for filename in files:
            match = id_pattern.search(filename)
            if match:
                all_ids.append(match.group(1))

    # Считаем дубликаты
    id_counts = Counter(all_ids)
    duplicates = {vid_id: count for vid_id, count in id_counts.items() if count > 1}

    # Добавляем уникальные ID этого языка в общий набор
    unique_ids.update(id_counts.keys())

    stats[lang] = {
        "total_files": len(all_ids),
        "unique_videos": len(id_counts),
        "duplicate_videos": len(duplicates),
        "duplicates": duplicates
    }

# Сохраняем список уникальных ID в файл
with open("unique_ids.txt", "w") as f:
    for uid in sorted(unique_ids):
        f.write(f"{uid}\n")

# Выводим статистику
for lang, data in stats.items():
    print(f"\n📂 Язык: {lang.upper()}")
    print(f"- Всего файлов (mp4/json): {data['total_files']}")
    print(f"- Уникальных видео (по ID): {data['unique_videos']}")
    print(f"- Дубликатов видео: {data['duplicate_videos']}")
    if data["duplicate_videos"]:
        print("  ⚠️ Повторяющиеся ID:")
        for vid_id, count in data["duplicates"].items():
            print(f"    - ID {vid_id} — {count} файлов")

print(f"\n📝 Уникальные ID сохранены в 'unique_ids.txt'")
print("✅ Проверка завершена.")
