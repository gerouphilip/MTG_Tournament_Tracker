This project is the results of a weekend Hackathon from 7/25/25 - 7/27/25
Authors Philip Gerou and Zachary Murphy

This program gathers Magic the Gathering tournament results listed by Top Deck, compiles the Top 8 deck lists for all events where the decks are listed, gathers all relevant information about the cards from Scryfall, and then process that information to give a breakdown on the color identity, converted Mana cost curve, and shows the 10 most commonly used cards of each format. 

All data has been gathered and charts have been created, but if you would like to run it yourself please follow the flow below.

First install all required packages from the requirements.txt

Gather tournament results by running tournament_decklists.py

combine all tournament results into 1 usable json per format with format_combine.py

Get a count on all cards in each format with card_count.py

get full card information for each card used in the tournaments from Scryfall.com with scryfall.py

process the gathered data with process_card_data.py

Generate the wanted style of graphs or top 10 card lists with the following: cmc_distribution_no_lands_summary.py, cmc_distribution_summary.py, color_identity_no_lands_summary.py, color_identity_summary.py, or most_popular_cards_summary.py

You can also search for specific cards within in a format by running card_representation.py and then inputting the format and card you are looking for. Both the format and the card name are case sensitive. 
