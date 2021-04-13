import random

class Library:
    """
    Class for loading and manipulating a deck copied via the MTG: Arena
    'Export Deck' feature.
    """
    def __init__(self, deck):
        """
        Takes the deck passed during the initialization of the class and creates
        five variables:
            - self.deck: Literally the raw text that was input
            - self.main_deck: A list of tuples of all cards in the main deck, with card count
            - self.sideboard: A list of tuples of all cards in the sideboard, with card count
            - self.decklist: A fully enmuerated decklist of self.main_deck
            - self.sideboardlist: A fully enmuerated decklist of self.sideboard
        """

        self.deck = [x.strip() for x in deck]
        self.main_deck = []
        self.sideboard = []
        
        if "Sideboard" in deck:
            sideboard_index = self.deck.index("Sideboard")

            self.sideboard = [ (int(x.split()[0]), ' '.join(x.split()[1:-2])) for x in self.deck[sideboard_index+1:] ]
            self.main_deck = [ (int(x.split()[0]), ' '.join(x.split()[1:-2])) for x in self.deck[1:sideboard_index] ] 
        else:
            self.main_deck = [ (int(x.split()[0]), ' '.join(x.split()[1:-2])) for x in self.deck[1:] ]

        self.decklist = self.make_deck_list(self.main_deck)
        self.decklist_backup = self.decklist.copy() # Create a backup copy so we can restore
        self.sideboardlist = self.make_deck_list(self.sideboard)
        self.sideboardlist_backup = self.sideboardlist.copy() # Create a backup copy so we can restore

    def make_deck_list(self, deck):
        """
        Takes a deck or sideboard that is a list of tuples,
        enumerates them, and returns the *full* list.

        (3, 'Plains') -> ['Plains', 'Plains', 'Plains']
        """
        decklist = []

        for card in deck:
            for i in range(card[0]):
                decklist.append(card[1])
        
        return decklist

    def draw(self, num_cards=1):
        """
        Draws <num_cards> cards off of the top of the library, shortens
        self.desklist by the number drawn
        """
        draw_cards = self.decklist[:num_cards]
        self.decklist = self.decklist[num_cards:]
        return draw_cards

    def shuffle(self):
        """
        Shuffles self.decklist
        """

        random.shuffle(self.decklist)

    def reset_deck(self):
        """
        Restores self.decklist and self.sideboardlist from the backup variables.
        """
        self.decklist = self.decklist_backup.copy()
        self.sideboardlist = self.sideboardlist_backup.copy()