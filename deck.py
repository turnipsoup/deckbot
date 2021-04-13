from src import library, librarian, painter

deck = [x.strip() for x in open('./deck.txt', 'r').readlines() if x != '\n']

library = library.Library(deck)

hands = []

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