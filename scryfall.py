import os
import json
import urllib.parse
import requests
import logging
import time

# Set up logging for debugging and info
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

base_url = "https://api.scryfall.com/cards/named?exact="
headers = {
    "Accept": "application/json",
    "User-Agent": "MTGTournamentTracker/1.0"
}

FORMAT = "Standard"
INPUT_FILE = f"data/{FORMAT}/cardcount_{FORMAT}.json"
OUTPUT_FILE = f"data/{FORMAT}/scryfall_{FORMAT}.json"

scryfall_data_dict = {}

# Retry parameters
MAX_RETRIES = 3
RETRY_DELAY = 2  # in seconds


def get_card_data():
    """Fetch card data from Scryfall and save it to a file."""
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info(f"Loaded {len(data)} card names from {INPUT_FILE}")

            for card_name, count in data.items():
                logging.info(f"Fetching data for card: {card_name}")
                card_data = fetch_card_data(card_name)
                if card_data:
                    scryfall_data_dict[card_name] = card_data
                time.sleep(1)  # Adding a small delay to avoid hitting rate limits

            write_data_to_file()

    except FileNotFoundError:
        logging.error(f"Input file {INPUT_FILE} not found.")
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from the file {INPUT_FILE}.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def fetch_card_data(card_name):
    """Fetch data for a single card from Scryfall."""
    retries = 0

    while retries < MAX_RETRIES:
        try:
            encoded_name = urllib.parse.quote_plus(card_name)
            request_url = f"{base_url}{encoded_name}"
            logging.debug(f"Requesting URL: {request_url}")

            response = requests.get(request_url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logging.warning(f"Card {card_name} not found in Scryfall.")
                return None
            else:
                logging.error(f"Failed to fetch data for {card_name}. HTTP status code: {response.status_code}")
                break  # Exit the retry loop for unexpected errors

        except requests.exceptions.RequestException as e:
            logging.warning(f"Request failed for {card_name}: {e}. Retrying...")
            retries += 1
            time.sleep(RETRY_DELAY)

    logging.error(f"Max retries reached for card: {card_name}")
    return None


def write_data_to_file():
    """Write the collected data to a JSON file."""
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(scryfall_data_dict, f, indent=4)
        logging.info(f"Data successfully written to {OUTPUT_FILE}")
    except IOError:
        logging.error(f"Failed to write data to {OUTPUT_FILE}.")
    except Exception as e:
        logging.error(f"An error occurred while saving the data: {e}")


if __name__ == "__main__":
    get_card_data()
