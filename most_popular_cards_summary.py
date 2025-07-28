import os
import json
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from urllib.request import urlopen
from PIL import Image
from io import BytesIO

DATA_DIR = "data"
CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

def load_top_cards(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    filtered_cards = []

    for card in cards.values():
        type_line = card.get("type_line")
        if isinstance(type_line, str) and "Basic Land" in type_line:
            continue

        count = card.get("count", 0)
        if count > 0:
            filtered_cards.append({
                "name": card.get("name", "Unknown"),
                "count": count,
                "image": card.get("image_uris", None)
            })

    total = sum(c["count"] for c in filtered_cards)
    top_10 = sorted(filtered_cards, key=lambda x: x["count"], reverse=True)[:10]

    for c in top_10:
        c["percent"] = 100 * c["count"] / total if total > 0 else 0

    return top_10

def plot_top_cards(top_cards, format_name):
    fig, ax = plt.subplots(figsize=(14, 8))
    names = [c["name"] for c in top_cards]
    percents = [c["percent"] for c in top_cards]

    bars = ax.bar(names, percents, color='mediumseagreen')
    ax.set_ylabel("Percentage of Total Cards (%)")
    ax.set_title(f"Top 10 Most Popular Cards (No Basic Lands) – {format_name}")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right')

    # Add images above bars
    for bar, card in zip(bars, top_cards):
        if not card["image"]:
            continue
        try:
            response = urlopen(card["image"])
            img_data = BytesIO(response.read())
            img = Image.open(img_data)
            imagebox = OffsetImage(img.resize((60, 85)), zoom=1)
            ab = AnnotationBbox(imagebox, (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                                frameon=False, xybox=(0, 40), xycoords='data', boxcoords="offset points")
            ax.add_artist(ab)
        except Exception as e:
            print(f"⚠️ Couldn't load image for {card['name']}: {e}")

    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, f"most_popular_{format_name}.png")
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

                top_cards = load_top_cards(file_path)
                if top_cards:
                    plot_top_cards(top_cards, format_name)

if __name__ == "__main__":
    main()
