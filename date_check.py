import os
import json
from datetime import datetime
from collections import defaultdict

base_dir = "data"
languages = ["en", "de", "ru"]
current_year = datetime.now().year

# Статистика по языкам
stats = defaultdict(lambda: {"total": 0, "not_current_year": 0})

for lang in languages:
    folder_path = os.path.join(base_dir, lang)

    if not os.path.exists(folder_path):
        print(f"⚠️ Папка '{lang}' не найдена, пропускаем.")
        continue

    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.endswith(".json"):
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                time_str = data["video_metadata"]["time_created"]
                video_year = datetime.fromisoformat(time_str).year

                stats[lang]["total"] += 1
                if video_year != current_year:
                    stats[lang]["not_current_year"] += 1

            except (KeyError, ValueError, json.JSONDecodeError) as e:
                print(f"⚠️ Ошибка обработки файла: {file_path} — {e}")

# Выводим статистику
print(f"\n📅 Статистика по годам (текущий год: {current_year}):")
for lang in languages:
    total = stats[lang]["total"]
    not_current = stats[lang]["not_current_year"]
    print(f"- {lang.upper()}: {not_current} из {total} видео не относятся к {current_year}")

print("\n✅ Проверка завершена.")
