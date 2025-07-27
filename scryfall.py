import json
import urllib.parse
import requests
import logging
import time
from constants import SUPPORTED_FORMATS, get_card_count_file_path_for, get_scryfall_file_path_for

# Set up logging for debugging and info
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

base_url = "https://api.scryfall.com/cards/named?exact="
headers = {
    "Accept": "application/json",
    "User-Agent": "MTGTournamentTracker/1.0"
}

# Retry parameters
MAX_RETRIES = 3
RETRY_DELAY = 2  # in seconds


def get_card_data(format_name):
    """Fetch card data from Scryfall and save it to a file."""
    scryfall_data_dict = {}
    input_file = get_card_count_file_path_for(format_name)
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info(f"Loaded {len(data)} card names from {input_file}")

            for card_name, count in data.items():
                logging.info(f"Fetching data for card: {card_name}")
                card_data = fetch_card_data(card_name)
                if card_data:
                    scryfall_data_dict[card_name] = card_data
                time.sleep(1)  # Adding a small delay to avoid hitting rate limits

            write_data_to_file(get_scryfall_file_path_for(format_name), scryfall_data_dict)

    except FileNotFoundError:
        logging.error(f"Input file {input_file} not found.")
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from the file {input_file}.")
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


def write_data_to_file(file_path, data):
    """Write the collected data to a JSON file."""

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data successfully written to {file_path}")
    except IOError:
        logging.error(f"Failed to write data to {file_path}.")
    except Exception as e:
        logging.error(f"An error occurred while saving the data: {e}")


if __name__ == "__main__":
    for format_name in SUPPORTED_FORMATS:
        get_card_data(format_name)
