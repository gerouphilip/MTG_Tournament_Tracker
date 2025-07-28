import os
import json
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt

def load_color_counts(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    color_counter = Counter()

    for card in cards.values():
        identity = card.get("color_identity") or []
        if not isinstance(identity, list):
            identity = []
        key = "".join(sorted(identity)) if identity else "Colorless"
        count = card.get("count", 1)
        color_counter[key] += count

    return color_counter

def plot_and_save_chart(counter, format_name):
    labels = list(counter.keys())
    sizes = list(counter.values())

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(f"Color Identity Distribution - {format_name}")
    plt.axis("equal")
    plt.tight_layout()

    chart_path = Path("charts")
    chart_path.mkdir(exist_ok=True)

    plt.savefig(chart_path / f"color_identity_{format_name}.png")
    plt.close()

def save_json(counter, format_name):
    chart_path = Path("charts")
    chart_path.mkdir(exist_ok=True)

    output_data = {color: count for color, count in counter.items()}
    output_file = chart_path / f"color_identity_{format_name}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

def main():
    base_folder = "data"
    chart_path = Path("charts")
    chart_path.mkdir(exist_ok=True)

    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        file_name = f"processed_{subfolder}.json"
        file_path = os.path.join(subfolder_path, file_name)

        if not os.path.exists(file_path):
            print(f"⚠️ Skipping {subfolder}: {file_name} not found.")
            continue

        print(f"📊 Processing format: {subfolder}")
        counter = load_color_counts(file_path)
        save_json(counter, subfolder)
        plot_and_save_chart(counter, subfolder)

if __name__ == "__main__":
    main()
