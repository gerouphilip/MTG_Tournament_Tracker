SUPPORTED_FORMATS = [
    "EDH", "Pauper EDH", "Standard", "Pioneer", "Modern", "Legacy", "Pauper", "Vintage", "Premodern",
    "Sealed", "Limited", "Duel Commander", "Canadian Highlander", "Tiny Leaders",
    "EDH Draft", "Timeless", "Historic", "Explorer", "7pt Highlander", "Oathbreaker"
]

DATA_DIR = "data"

def get_card_count_file_path_for(format_name):
    return f"data/{format_name}/cardcount_{format_name}.json"

def get_combined_file_path_for(format_name):
    return f"data/{format_name}/combined_{format_name}.json"

def get_scryfall_file_path_for(format_name):
    return f"data/{format_name}/scryfall_{format_name}.json"