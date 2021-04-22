import random, math
import numpy as np
from . import setup_logger

logger = setup_logger.logger


class Librarian:
    def __init__(self, hands, library):
        '''
        Takes a lists of lists of cards.
        Generally this is just hands (7 cards), but you can get weird if you want.
        
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

    def clean_values(self, values_dict, remove_value=0.0):
        # Remove values that are not wanted in a dictionary
        clean_averages = {}
        for k,v in values_dict.items():
            if v != remove_value:
                clean_averages[k] = v

        return clean_averages

    def average_all_selected(self, checklist=[]):
        '''
        1. Takes a list of hands/cards
        2. Takes a list of card names to get an average of their presence 
        in each object over the entire list of lists

        By default it does everything that is not a land card in self.library.decklist
        '''

        cards = {}

        # If checklist is blank, by default check all non-land cards.
        if len(checklist) < 1:

            for card in self.library.decklist:
                if card not in self.basic_lands:
                    if 'Land' not in self.library.card_details[card].types:
                        checklist.append(card)

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

        return averages

    def average_all_lands(self):
        '''
        Runs self.average_all_selected but for only land types.
        '''
        lands = self.basic_lands

        for card in self.library.card_details:
            if "Land" in self.library.card_details[card].types:
                lands.append(card)

        averages = self.average_all_selected(lands)

        return averages

    def sample_hands(self, num_hands=5):
        '''
        Returns the top X hands of the self.hands.
        '''
        return self.hands[:num_hands]

    def cmc_details(self, hand):
        """
        Returns a tuple containing the following:
        (average_hand_cmc, total_hand_cmc)
        """

        cmc = 0
        hand_length = len(hand)

        for card in hand:
            cmc += self.library.card_details[card].cmc
        
        return (cmc / hand_length, cmc)