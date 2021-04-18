from . import library, librarian, card, painter
import logging

class Mage:
    def __init__(self, message, config):
        self.message = message
        self.config = config
        self.known_methods = [
            "landavg",
            "nonlandavg",
            "fullavg",
            "cardinfo"
        ]

        # Define and clean the deck
        self.deck = deck = self.message.replace(self.config['call_name'], '')
        
        for method in self.known_methods:
            self.deck = self.deck.replace(method, '')
        
        self.deck =  [x for x in self.deck.split("\n") if len(x) > 1]


        self.deck_library = library.Library(self.deck, self.config)

    def draw_hands(self):
        '''
        Draw a number of hands equal to the iterations value in config
        '''

        # Initiate global
        hands = []

        # Draw configured number of times
        for i in range(self.config['iterations']):
            self.deck_library.shuffle()
            hands.append(self.deck_library.draw(7))
            self.deck_library.reset_deck()

        return hands

    def get_land_average(self):
        '''
        If the user requests an average of lands per hand
        '''

        hands = self.draw_hands()

        self.deck_librarian = librarian.Librarian(hands, self.deck_library)
        averages = self.deck_librarian.average_all_lands()

        clean_averages = self.deck_librarian.clean_values(averages)

        # Pretty it up even more
        final_mage_response = f'Average Land Per Starting Hand Over {self.config["iterations"]} Draws\n--------\n'
        for result in clean_averages.keys():
            if result != 'total':
                final_mage_response += f'\t{result}: {clean_averages[result]}\n'
            else:
                final_mage_response += f'Total: {clean_averages[result]}\n'

        return final_mage_response

    def get_specific_average(self, decklist=[]):
        '''
        If the user requests an average of lands per hand
        '''

        hands = self.draw_hands()

        self.deck_librarian = librarian.Librarian(hands, self.deck_library)
        averages = self.deck_librarian.average_all_selected()

        clean_averages = self.deck_librarian.clean_values(averages)

        # Pretty it up even more
        final_mage_response = f'Average Non-Land Card Per Starting Hand Over {self.config["iterations"]} Draws\n--------\n'
        for result in clean_averages.keys():
            if result != 'total':
                final_mage_response += f'\t{result}: {clean_averages[result]}\n'
            else:
                final_mage_response += f'Total: {clean_averages[result]}\n'

        return final_mage_response

    def get_sample_hands(self, num_hands=5):
        '''
        Return X sample hands (7 card hands)
        '''
        hands = self.draw_hands()
        self.deck_librarian = librarian.Librarian(hands, self.deck_library)
        sample_hands = self.deck_librarian.sample_hands(num_hands)

        final_mage_response = 'Sample Hands\n--------\n'

        for hand in sample_hands:
                final_mage_response += ', '.join(sorted(hand)) + '\n\n'

        return final_mage_response

    def get_card_info(self):
        '''
        Return info for a single card
        '''
        final_mage_response = 'Card Info\n--------\n'
        mtgcard = card.Card(self.config, ' '.join(self.message.split()[2:]))

        final_mage_response += 'Name: ' + mtgcard.name + '\n'
        final_mage_response += '\t' + 'Types: ' + ', '.join(mtgcard.types) + '\n'
        final_mage_response += '\t' + 'Mana Cost: ' + ''.join(mtgcard.mana_cost) + '\n'
        final_mage_response += '\t' + 'CMC: ' + str(mtgcard.cmc) + '\n'
        final_mage_response += '\t' + 'P/T: ' + str(mtgcard.power) + '/' + str(mtgcard.toughness) + '\n'
        final_mage_response += '\t' + 'Text: ' + str(mtgcard.text) + '\n'
        final_mage_response += '\t' + 'Rarity: ' + str(mtgcard.rarity) + '\n'

        return final_mage_response