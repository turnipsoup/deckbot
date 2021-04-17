from . import library, librarian, card, painter

class Mage:
    def __init__(self, message, config):
        self.message = message
        self.config = config

    def get_land_average(self):
        '''
        If the user requests an average of lands per hand
        '''
        deck = self.message.replace(self.config['call_name'], '').replace('landavg', '')
        deck = [x for x in deck.split("\n") if len(x) > 1]
        deck_library = library.Library(deck, self.config)

        # Initiate global
        hands = []

        # Draw configured number of times
        for i in range(self.config['iterations']):
            deck_library.shuffle()
            hands.append(deck_library.draw(7))
            deck_library.reset_deck()

        deck_librarian = librarian.Librarian(hands, deck_library)
        averages = deck_librarian.average_all_lands()

        # Remove cards that were not even drawn, thus probably do not exist.
        clean_averages = {}
        for k,v in averages.items():
            if v != 0.0:
                clean_averages[k] = v

        return clean_averages