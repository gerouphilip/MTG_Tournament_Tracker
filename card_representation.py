import json
import os
import sys

def load_card_data(format_name):
    file_path = f"data/{format_name}/cardcount_{format_name}.json"

    if not os.path.exists(file_path):
        print(f"Error: File not found for format '{format_name}' at '{file_path}'")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON: {e}")
        sys.exit(1)


def calculate_representation(card_name, format_name):
    card_data = load_card_data(format_name)

    total_card_count = sum(card_data.values())
    card_count = card_data.get(card_name, 0)

    if card_count == 0:
        print(f"'{card_name}' does not appear in the data for format '{format_name}'.")
        return

    representation = (card_count / total_card_count) * 100

    print(f"Card: {card_name}")
    print(f"Format: {format_name}")
    print(f"Count: {card_count}")
    print(f"Total Cards: {total_card_count}")
    print(f"Representation: {representation:.2f}%")



# ---- Entry Point ----
if __name__ == "__main__":
    # Simple input prompt; you can replace this with argparse if preferred
    format_input = input("Enter format (e.g. Standard): ").strip()
    card_name_input = input("Enter card name: ").strip()

    calculate_representation(card_name_input, format_input)
