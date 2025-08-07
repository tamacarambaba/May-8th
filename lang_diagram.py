import matplotlib.pyplot as plt

# Укажи путь к текстовому файлу
input_file = r"D:\PS Data\language distribution (new).txt"

min_percentage_named = 2.0

languages = []
counts = []
percentages = []

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            lang = parts[0].rstrip(":")
            count = int(parts[1].strip("()"))
            percent = float(parts[2].strip("()%"))
            languages.append(lang)
            counts.append(count)
            percentages.append(percent)

# Сортировка
combined = sorted(zip(languages, counts, percentages), key=lambda x: x[1], reverse=True)

# Построение списков для диаграммы
labels = []
sizes = []
other_total = 0

for i, (lang, count, percent) in enumerate(combined):
    if percent >= min_percentage_named:
        labels.append(lang)
        sizes.append(percent)
    else:
        other_total += percent

if other_total > 0:
    labels.append("Other")
    sizes.append(other_total)

# Построение диаграммы
plt.figure(figsize=(10, 8))
colors = plt.get_cmap("tab20").colors

plt.pie(
    sizes,
    labels=labels,
    startangle=140,
    colors=colors,
    wedgeprops={'edgecolor': 'white'}
)

plt.axis("equal")
plt.title("Language Distribution in Dataset")
plt.tight_layout()
plt.show()
