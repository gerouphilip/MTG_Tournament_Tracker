import os
import json
from constants import SUPPORTED_FORMATS, get_combined_file_path_for

def combine_decklists_for(format_name):
    combined_entries = []
    # Traverse all JSON files in the folder
    input_folder = f"data/{format_name}"

    for filename in os.listdir(input_folder):
        if filename.startswith("cardcount") or (filename.startswith("combined")):
            continue

        if filename.endswith(".json"):
            filepath = os.path.join(input_folder, filename)
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
    output_file = get_combined_file_path_for(format_name)
    # Save to output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined_entries, f, indent=2)

    print(f"✅ Combined {len(combined_entries)} entries saved to {output_file}")

def combine_format_data():
    for format_name in SUPPORTED_FORMATS:
        combine_decklists_for(format_name)


# ---- Entry Point ----
if __name__ == "__main__":
    combine_format_data()