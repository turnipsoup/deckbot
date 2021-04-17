from src import library, librarian, painter, card
import sqlite3, os, logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s|%(levelname)s|%(message)s"
    )


# Check if this is first run and create a cache directory

cache_dir = "./cache"
if os.path.isdir(cache_dir):
    pass
else:
    os.mkdir(cache_dir)

# Define the raw deck
deck = [x.strip() for x in open('./deck.txt', 'r').readlines() if x != '\n']

# Create the library from the raw deck
library = library.Library(deck)

# Initiate global
hands = []

# Draw 100000 times
for i in range(10000):
    library.shuffle()
    hands.append(library.draw(7))
    library.reset_deck()

custom_defs = {
    'land': ['Needleverge Pathway', 'Wind-Scarred Crag']
    }

librarian = librarian.Librarian(hands, custom_defs)

averages, totals = librarian.average_all_selected()

print(averages)

for mtgcard in library.decklist:

    testcard = card.Card(mtgcard)
    print(testcard.cmc)