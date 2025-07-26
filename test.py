import os
import json

DATA_DIR = "data"

# Walk through each subfolder in the data directory
for root, dirs, files in os.walk(DATA_DIR):
    # Skip the root itself, only process subfolders
    if root == DATA_DIR:
        continue

    format_name = os.path.basename(root)
    combined_entries = []

    for filename in files:
        if filename.endswith(".json"):
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    tournament = json.load(f)
                    top8 = tournament.get("top_8", [])

                    valid_players = [
                        {
                            "tournament_name": tournament.get("tournament_name", "Unknown"),
                            "format": tournament.get("format", format_name),
                            "date": tournament.get("date", "Unknown"),
                            "rank": player.get("rank"),
                            "decklist": player.get("decklist")
                        }
                        for player in top8
                        if player.get("decklist") and player["decklist"] != "No decklist available"
                    ]

                    combined_entries.extend(valid_players)

            except json.JSONDecodeError:
                print(f"⚠️ Failed to parse: {filepath}")

    if combined_entries:
        output_file = os.path.join(root, f"combined_{format_name}.json")
        with open(output_file, "w", encoding="utf-8") as f_out:
            json.dump(combined_entries, f_out, indent=2)
        print(f"✅ Saved {len(combined_entries)} entries to {output_file}")
    else:
        print(f"📭 No valid entries found in {format_name}, skipping output.")
