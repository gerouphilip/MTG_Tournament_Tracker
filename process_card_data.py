import os
import json

# Fields to extract from scryfall data
SCRYFALL_FIELDS = [
    "name",
    "image_uris",
    "mana_cost",
    "cmc",
    "colors",
    "color_identity",
    "rarity",
    "type_line"
]

def extract_scryfall_data(scryfall_path):
    with open(scryfall_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    filtered_data = {}
    for card_name, card_data in raw_data.items():
        filtered = {field: card_data.get(field) for field in SCRYFALL_FIELDS}
        if "image_uris" in filtered and isinstance(filtered["image_uris"], dict):
            filtered["image_uris"] = filtered["image_uris"].get("normal", None)
        filtered_data[card_name] = filtered

    return filtered_data

def merge_with_card_counts(scryfall_data, card_counts_path):
    with open(card_counts_path, "r", encoding="utf-8") as f:
        card_counts = json.load(f)

    for card_name, count in card_counts.items():
        if card_name in scryfall_data:
            scryfall_data[card_name]["count"] = count
        else:
            # Add as unknown if not in Scryfall data
            scryfall_data[card_name] = {
                "name": card_name,
                "image_uris": None,
                "mana_cost": None,
                "cmc": None,
                "colors": None,
                "color_identity": None,
                "rarity": None,
                "type_line": None,
                "count": count
            }

    return scryfall_data

def process_format_folder(folder_path, format_name):
    scryfall_file = os.path.join(folder_path, f"scryfall_{format_name}.json")
    cardcount_file = os.path.join(folder_path, f"cardcount_{format_name}.json")
    output_file = os.path.join(folder_path, f"processed_{format_name}.json")

    if not os.path.exists(scryfall_file):
        print(f"⚠️ Missing scryfall data for {format_name}")
        return
    if not os.path.exists(cardcount_file):
        print(f"⚠️ Missing card count data for {format_name}")
        return

    print(f"📁 Processing {format_name}")
    scryfall_data = extract_scryfall_data(scryfall_file)
    combined_data = merge_with_card_counts(scryfall_data, cardcount_file)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Output written to {output_file}")

def main():
    base_folder = "data"

    for format_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, format_name)
        if os.path.isdir(folder_path):
            process_format_folder(folder_path, format_name)

if __name__ == "__main__":
    main()