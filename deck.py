from src import library, librarian, painter, card
import sqlite3, os, logging, json

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s|%(levelname)s|%(message)s"
    )

# Load config file
config = json.loads(open("./config/config.json", "r").read())

# Define the raw deck
deck = [x.strip() for x in open('./deck.txt', 'r').readlines() if x != '\n']

# Create the library from the raw deck
library = library.Library(deck, config)

# Initiate global
hands = []

# Draw 100000 times
for i in range(config['iterations']):
    library.shuffle()
    hands.append(library.draw(7))
    library.reset_deck()

custom_defs = {
    'land': ['Needleverge Pathway', 'Wind-Scarred Crag']
    }

librarian = librarian.Librarian(hands, custom_defs)

averages, totals = librarian.average_all_selected()

print(averages)

print(len(library.card_details.keys()))
