from src import library, librarian

deck = [x.strip() for x in open('./deck.txt', 'r').readlines() if x != '\n']

library = library.Library(deck)

hands = []

for i in range(10000):
    library.shuffle()
    hands.append(library.draw(7))
    library.reset_deck()

librarian = librarian.Librarian(hands, {'land': ['Needleverge Pathway', 'Wind-Scarred Crag']})

print(librarian.average_all_selected())
