import os
import json

# === CONFIGURATION ===
INPUT_FOLDER = "data/Standard"  # Change to your target folder
OUTPUT_FILE = "combined_decklists.json"

combined_entries = []

# Traverse all JSON files in the folder
for filename in os.listdir(INPUT_FOLDER):
    if filename.startswith("cardcount") or (filename.startswith("combined")):
        continue

    if filename.endswith(".json"):
        filepath = os.path.join(INPUT_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                tournament = json.load(f)
                top8 = tournament.get("top_8", [])

                # Keep only players with valid decklists
                valid_decklists = [
                    {
                        "tournament_name": tournament.get("tournament_name", "Unknown"),
                        "format": tournament.get("format", "Unknown"),
                        "date": tournament.get("date", "Unknown"),
                        "rank": player.get("rank"),
                        "decklist": player.get("decklist")
                    }
                    for player in top8
                    if player.get("decklist") and player["decklist"] != "No decklist available"
                ]

                combined_entries.extend(valid_decklists)
            except json.JSONDecodeError:
                print(f"⚠️ Failed to parse JSON: {filename}")

# Save to output file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(combined_entries, f, indent=2)

print(f"✅ Combined {len(combined_entries)} entries saved to {OUTPUT_FILE}")
