import random, math
import numpy as np

class Librarian:
    def __init__(self, hands, library, custom_defs={}):
        '''
        Takes a lists of lists of cards.
        Generally this is just hands (7 cards), but you can get weird if you want.
        
        self.custom_defs lets you label cards specifically, such as:
            {Lands: }
        '''
        self.name = 'Librarian'
        self.hands = hands
        self.library = library
        self.basic_lands = [
            'Plains',
            'Mountain',
            'Forest',
            'Swamp',
            'Island',
            'Snow-Covered Plains',
            'Snow-Covered Mountain',
            'Snow-Covered Forest',
            'Snow-Covered Swamp',
            'Snow-Covered Island'
        ]
        self.custom_defs = custom_defs

    def average_all_selected(self, checklist=[]):
        '''
        1. Takes a list of hands/cards
        2. Takes a list of card names to get an average of their presence 
        in each object over the entire list of lists

        By default it does everything that is defined as a Basic Land card.
        '''

        cards = {}

        # Raw count
        for card in checklist:
            count = 0
            cards[card] = []
            for hand in self.hands:
                cards[card].append(hand.count(card))

        # Average each
        averages = {}
        averages['total'] = 0

        for card in cards:
            averages[card]  = np.mean(cards[card])
            averages['total'] += averages[card]

        return averages, cards

    def average_all_selected_lands(self):
