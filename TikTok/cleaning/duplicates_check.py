import os
import re
from collections import Counter

# Путь к основной папке
base_dir = "data"
languages = ["en", "de", "ru"]

# Регулярка для извлечения TikTok ID
id_pattern = re.compile(r"tiktok_(\d+)_")

# Загружаем уже сохранённые ID (если файл существует)
existing_ids = set()
if os.path.exists("unique_ids.txt"):
    with open("unique_ids.txt", "r") as f:
        existing_ids = set(line.strip() for line in f if line.strip())

# Для хранения статистики и всех уникальных ID
stats = {}
new_unique_ids = set()

for lang in languages:
    folder_path = os.path.join(base_dir, lang)
    all_ids = []

    if not os.path.exists(folder_path):
        print(f"⚠️ Папка '{lang}' не найдена, пропускаем.")
        continue

    for root, _, files in os.walk(folder_path):
        for filename in files:
            match = id_pattern.search(filename)
            if match:
                all_ids.append(match.group(1))

    id_counts = Counter(all_ids)
    duplicate_count = sum(count - 1 for count in id_counts.values() if count > 1)

    # Отбираем только ID, которых ещё не было
    new_ids_for_lang = set(id_counts.keys()) - existing_ids
    new_unique_ids.update(new_ids_for_lang)

    stats[lang] = {
        "total_files": len(all_ids),
        "unique_videos": len(id_counts),
        "duplicate_videos": duplicate_count,
        "new_ids": len(new_ids_for_lang),
    }

# Добавляем новые уникальные ID в файл (дописываем)
if new_unique_ids:
    with open("unique_ids.txt", "a") as f:
        for uid in sorted(new_unique_ids):
            f.write(f"{uid}\n")

# Выводим статистику
for lang, data in stats.items():
    print(f"\n📂 Язык: {lang.upper()}")
    print(f"- Всего файлов (mp4/json): {data['total_files']}")
    print(f"- Уникальных видео (по ID): {data['unique_videos']}")
    print(f"- Повторяющихся файлов: {data['duplicate_videos']}")
    print(f"- Новых ID добавлено: {data['new_ids']}")

print(f"\n📝 Добавлено {len(new_unique_ids)} новых уникальных ID в 'unique_ids.txt'")
print("✅ Проверка завершена.")
