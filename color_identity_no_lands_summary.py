import os
import json
from collections import Counter
import matplotlib.pyplot as plt

DATA_DIR = "data"
CHARTS_DIR = "charts"

def load_color_counts(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    color_counter = Counter()

    for card in cards.values():
        type_line = card.get("type_line")
        if isinstance(type_line, str) and "Land" in type_line:
            continue  # Skip lands

        identity = card.get("color_identity") or []
        if not isinstance(identity, list):
            identity = []
        key = "".join(sorted(identity)) if identity else "Colorless"
        count = card.get("count", 1)
        color_counter[key] += count

    return color_counter

def plot_pie_chart(counter, format_name):
    if not os.path.exists(CHARTS_DIR):
        os.makedirs(CHARTS_DIR)

    labels = []
    sizes = []
    for identity, count in counter.items():
        labels.append(identity)
        sizes.append(count)

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(f"Color Identity Distribution (No Lands) - {format_name}")
    filename = os.path.join(CHARTS_DIR, f"color_identity_no_lands_{format_name}.png")
    plt.savefig(filename)
    plt.close()

    # Save as JSON summary too
    json_filename = os.path.join(CHARTS_DIR, f"color_identity_no_lands_{format_name}.json")
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(dict(counter), f, indent=2)

def main():
    for subfolder in os.listdir(DATA_DIR):
        subfolder_path = os.path.join(DATA_DIR, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        for filename in os.listdir(subfolder_path):
            if filename.startswith("processed_") and filename.endswith(".json"):
                file_path = os.path.join(subfolder_path, filename)
                format_name = filename.removeprefix("processed_").removesuffix(".json")
                counter = load_color_counts(file_path)
                plot_pie_chart(counter, format_name)
                print(f"✅ Processed {format_name}")

if __name__ == "__main__":
    main()
