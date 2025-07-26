import os
import requests
import json
import re

# === Configuration ===
API_KEY = "e5287194-938e-4c24-958d-90c5d6f6890d"


# === Supported Formats ===
SUPPORTED_FORMATS = [
    "EDH", "Pauper EDH", "Standard", "Pioneer", "Modern", "Legacy", "Pauper", "Vintage", "Premodern",
    "Sealed", "Limited", "Duel Commander", "Old School 93/94", "Canadian Highlander", "Tiny Leaders",
    "EDH Draft", "Timeless", "Historic", "Explorer", "7pt Highlander", "Oathbreaker"
]

# === Prompt for Format ===
print("Available Tournament Formats:")
for i, fmt in enumerate(SUPPORTED_FORMATS, start=1):
    print(f"  {i}. {fmt}")

while True:
    user_input = input("Enter the tournament format name exactly as shown above: ").strip()
    if user_input in SUPPORTED_FORMATS:
        TOURNAMENT_FORMAT = user_input
        break
    else:
        print("❌ Invalid format. Please try again and type exactly as shown.")

# Create output directory if it doesn't exist
OUTPUT_DIR = os.path.join("data", TOURNAMENT_FORMAT)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Request Setup ===
headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

url = "https://topdeck.gg/api/v2/tournaments"

payload = {
    "last": 1000,
    "game": "Magic: The Gathering",
    "format": TOURNAMENT_FORMAT,
    "participantMin": 8,
    "columns": ["decklist"],
    "rounds": False
}

# === Make API Call ===
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Tournaments retrieved:", len(data))

    for index, tournament in enumerate(data):
        # Extract fields
        raw_name = tournament.get("name")
        date_raw = tournament.get("date", "")
        tid = tournament.get("id", "")
        fmt = tournament.get("format", "UnknownFormat")

        # Clean components
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', raw_name) if raw_name else "Unnamed_Tournament"
        safe_date = re.sub(r'[^0-9]', '', date_raw)[:8] if date_raw else "00000000"
        safe_tid = tid[:8] if tid else f"{index:03d}"
        safe_format = re.sub(r'[^a-zA-Z0-9_\-]', '_', fmt)

        filename = f"{safe_name}_{safe_format}_{safe_date}_{safe_tid}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)

        standings = tournament.get("standings", [])[:8]

        # Structure data
        top8_info = {
            "tournament_name": raw_name or f"Unnamed Tournament {safe_tid}",
            "format": fmt,
            "date": date_raw or "Unknown Date",
            "top_8": []
        }

        has_valid_decklist = False

        for i, player in enumerate(standings, start=1):
            deck = player.get("decklist")

            if deck:  # non-null and non-empty
                has_valid_decklist = True

            player_data = {
                "rank": i,
                "decklist": deck or "No decklist available"
            }
            top8_info["top_8"].append(player_data)

        if has_valid_decklist:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(top8_info, f, indent=2)
            print(f"✅ Saved: {filepath}")
        else:
            print(f"⏭️ Skipped: {safe_name} — no valid decklists.")