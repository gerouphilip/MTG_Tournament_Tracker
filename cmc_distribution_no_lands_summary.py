import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt

DATA_DIR = "data"
CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

def load_cmc_counts(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    cmc_counter = defaultdict(int)

    for card in cards.values():
        type_line = card.get("type_line", "")
        if type_line is None or "Land" in type_line:
            continue

        cmc = card.get("cmc")
        count = card.get("count", 1)

        if cmc is not None:
            try:
                cmc = int(cmc)
            except (ValueError, TypeError):
                cmc = int(float(cmc)) if cmc else 0
            cmc_counter[cmc] += count

    return cmc_counter

def plot_cmc_bar(cmc_counter, format_name):
    sorted_items = sorted(cmc_counter.items())
    cmcs = [k for k, _ in sorted_items]
    counts = [v for _, v in sorted_items]

    plt.figure(figsize=(10, 6))
    plt.bar(cmcs, counts, color="skyblue", edgecolor="black")
    plt.xlabel("Converted Mana Cost (CMC)")
    plt.ylabel("Card Count")
    plt.title(f"CMC Distribution (No Lands) – {format_name}")
    plt.xticks(cmcs)

    out_path = os.path.join(CHARTS_DIR, f"cmc_distribution_{format_name}_no_lands.png")
    plt.savefig(out_path)
    plt.close()
    print(f"✅ Saved: {out_path}")

def main():
    for subfolder in os.listdir(DATA_DIR):
        subfolder_path = os.path.join(DATA_DIR, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        for file in os.listdir(subfolder_path):
            if file.startswith("processed_") and file.endswith(".json"):
                format_name = file.removeprefix("processed_").removesuffix(".json")
                file_path = os.path.join(subfolder_path, file)

                counter = load_cmc_counts(file_path)
                plot_cmc_bar(counter, format_name)

if __name__ == "__main__":
    main()
