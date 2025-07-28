import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

DATA_DIR = "data"
CHARTS_DIR = "charts"

os.makedirs(CHARTS_DIR, exist_ok=True)

def load_cmc_counts(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    cmc_counter = defaultdict(int)

    for card in cards.values():
        cmc = card.get("cmc")
        count = card.get("count", 1)

        if cmc is None or not isinstance(cmc, (int, float)):
            continue

        cmc = int(round(cmc))  # Round to nearest int
        cmc_counter[cmc] += count

    return cmc_counter

def plot_cmc_distribution(format_name, cmc_counter):
    sorted_cmc = sorted(cmc_counter.items())
    x = [str(cmc) for cmc, _ in sorted_cmc]
    y = [count for _, count in sorted_cmc]

    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color="skyblue")
    plt.xlabel("Converted Mana Cost (CMC)")
    plt.ylabel("Card Count")
    plt.title(f"CMC Distribution – {format_name}")
    plt.tight_layout()

    out_path = os.path.join(CHARTS_DIR, f"cmc_distribution_{format_name}.png")
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

                cmc_counter = load_cmc_counts(file_path)
                plot_cmc_distribution(format_name, cmc_counter)

if __name__ == "__main__":
    main()
