from . import library, librarian, card, painter

class Mage:
    def __init__(self, message, config):
        self.message = message
        self.config = config
        self.known_methods = [
            "landavg",
            "nonlandavg",
            "fullavg"
        ]

        # Define and clean the deck
        self.deck = deck = self.message.replace(self.config['call_name'], '').replace('landavg', '')
        
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