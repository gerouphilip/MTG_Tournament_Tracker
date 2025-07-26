import os
import json
import re
from collections import defaultdict

DATA_DIR = "data"

def extract_card_counts(decklist_text):
    card_counts = defaultdict(int)
    lines = decklist_text.replace("\\n", "\n").split("\n")

    for line in lines:
        line = line.strip()
        if not line or line.startswith("~~"):
            continue
        match = re.match(r"^(\d+)\s+(.+?)$", line)
        if match:
            count = int(match.group(1))
            card = match.group(2).strip()
            card_counts[card] += count
    return card_counts

def process_json_file(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_counts = defaultdict(int)

    for entry in data:
        decklist = entry.get("decklist", "")
        if not decklist.startswith("http"):
            card_counts = extract_card_counts(decklist)
            for card, count in card_counts.items():
                total_counts[card] += count

    return total_counts

def main():
    for subfolder in os.listdir(DATA_DIR):
        subfolder_path = os.path.join(DATA_DIR, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        input_filename = f"combined_{subfolder}.json"
        input_path = os.path.join(subfolder_path, input_filename)

        if not os.path.exists(input_path):
            print(f"❌ Skipping {subfolder}: file {input_filename} not found")
            continue

        print(f"📦 Processing {input_filename}...")

        card_counts = process_json_file(input_path)

        sorted_counts = dict(sorted(card_counts.items(), key=lambda x: x[1], reverse=True))

        output_filename = f"cardcount_{subfolder}.json"
        output_path = os.path.join(subfolder_path, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sorted_counts, f, indent=2)

        print(f"✅ Saved to {output_filename}\n")

if __name__ == "__main__":
    main()
