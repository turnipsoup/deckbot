from . import library, librarian, card, painter
from . import setup_logger
import json, requests, sqlite3
import bs4 as bs

logger = setup_logger.logger

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
        
        # Initiate cards.db if it does not exist
        db = f'{self.config["cache_dir"]}/cards.db'
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        try:
            cursor.execute('''CREATE TABLE cards (name TEXT, path TEXT)''')
            logger.info(f'Created database {db}')
            connection.close()
        except:
            logger.debug(f'Database {db} already exists, loading!')
            connection.close()


        # Library
        self.deck =  [x for x in self.deck.split("\n") if len(x) > 1]
        self.deck_library = library.Library(self.deck, self.config)
        self.fully_loaded = False
        

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

        self.hands = hands

    def fully_load(self):
        '''
        Create the hands librarian, basically
        '''

        self.draw_hands()
        self.deck_librarian = librarian.Librarian(self.hands, self.deck_library)
        self.fully_loaded = True
        logger.debug("Fully loaded the librarian")

    def get_land_average(self):
        '''
        If the user requests an average of lands per hand
        '''

        try:
            if not self.fully_loaded:
                self.fully_load()
        except:
            logger.exception("Something went wrong looking for a hand")

        averages = self.deck_librarian.average_all_lands()
        clean_averages = self.deck_librarian.clean_values(averages)

        # Pretty it up even more
        final_mage_response = f'**Average Land Per Starting Hand Over {self.config["iterations"]} Draws**\n--------\n'
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

        try:
            if not self.fully_loaded:
                self.fully_load()
        except:
            logger.exception("Something went wrong looking for a hand")

        
        averages = self.deck_librarian.average_all_selected()
        clean_averages = self.deck_librarian.clean_values(averages)

        # Pretty it up even more
        final_mage_response = f'**Average Non-Land Card Per Starting Hand Over {self.config["iterations"]} Draws**\n--------\n'

        try:
            for result in clean_averages.keys():
                if result != 'total':
                    final_mage_response += f'\t{result}: {clean_averages[result]}\n'
                else:
                    final_mage_response += f'Total: {clean_averages[result]}\n'
        except:
            logger.exception("Something went wrong getting sample hands!")
            final_mage_response += "Something went wrong getting sample hands. Please contact the admin!"

        return final_mage_response

    def get_sample_hands(self, num_hands=5):
        '''
        Return X sample hands (7 card hands)
        '''

        try:
            if not self.fully_loaded:
                self.fully_load()
        except:
            logger.exception("Something went wrong drawing hands")

        sample_hands = self.deck_librarian.sample_hands(num_hands)


        final_mage_response = '**Sample Hands**\n--------\n'
        try:
            for hand in sample_hands:
                    final_mage_response += ', '.join(sorted(hand)) + '\n\n'
        except:
            logger.exception("Something went wrong getting sample hands!")
            final_mage_response += "Something went wrong getting sample hands. Please contact the admin!"

        return final_mage_response

    def get_card_info(self):
        '''
        Return info for a single card
        '''
        final_mage_response = 'Card Info\n--------\n'
        mtgcard = card.Card(self.config, ' '.join(self.message.split()[2:]))

        try:

            final_mage_response += '**Name**: ' + mtgcard.name + '\n'
            final_mage_response += '\t' + '**Types**: ' + ', '.join(mtgcard.types) + '\n'

            if mtgcard.mana_cost != None:
                final_mage_response += '\t' + '**Mana Cost**: ' + ''.join(mtgcard.mana_cost) + '\n'
            else:
                final_mage_response += '\t' + '**Mana Cost**: ' + ' None' + '\n'

            final_mage_response += '\t' + '**CMC**: ' + str(mtgcard.cmc) + '\n'
            final_mage_response += '\t' + '**P/T**: ' + str(mtgcard.power) + '/' + str(mtgcard.toughness) + '\n'
            final_mage_response += '\t' + '**Text**: ' + str(mtgcard.text) + '\n'
            final_mage_response += '\t' + '**Flavor**: ' + str(mtgcard.flavor) + '\n'
            final_mage_response += '\t' + '**Rarity**: ' + str(mtgcard.rarity) + '\n'
            final_mage_response += '\t' + '**Image URL**: ' + str(mtgcard.image_url) + '\n'

        except:
            logger.exception(f"There was an error defining card {mtgcard.name}!")
            final_mage_response = f"There was an error requesting {mtgcard.name}. Please ensure it exists, and your spelling is correct."

        return final_mage_response

    def get_keyword_definition(self):
        """
        Define a keyword that is stored in <config-dir>/mtg-keyword-defs.json
        """

        try:
            keywords = json.loads(open(self.config['mtg_keywords_file'], 'r').read())
            mtgkeyword = ' '.join(self.message.split()[2:]).lower()

            final_mage_response = f'**{mtgkeyword.capitalize()}**\n--------\n'
            final_mage_response += f'> {keywords[mtgkeyword]}'

        except:
            logger.exception("Unable to define keyword!")

            mtgkeyword = ' '.join(self.message.split()[2:]).lower()
            final_mage_response = f'**{mtgkeyword.capitalize()}**\n--------\n'

            final_mage_response += "There was an error defining the word, please check your spelling. If you are certain the spelling is correct, please contact the admin."

        return final_mage_response

    def get_average_hand_cmc(self):
        """
        Will get the average/total CMC for ALL hands in self.hands and return that
        single value.
        """

        try:

            total_avg_cmc = 0
            average_avg_cmc = 0

            for hand in self.hands:
                hand_cmcs = self.deck_librarian.cmc_details(hand)
                average_avg_cmc += hand_cmcs[0]
                total_avg_cmc += hand_cmcs[1]

            total_avg_cmc = total_avg_cmc / len(self.hands)
            average_avg_cmc = average_avg_cmc / len(self.hands)

            final_mage_response = '**Hand CMC Averages**:\n--------\n'
            final_mage_response += f'Average CMC Per Card In Hand: {average_avg_cmc}\n'
            final_mage_response += f'Average Total Hand CMC: {total_avg_cmc}\n'

        except:
            logger.exception("There was an error defining CMC!")
            final_mage_response = "There was an error defining CMC, please contact an admin!"

        return final_mage_response

    def update_keyword_definitions(self):

        try:
            # The wiki page
            WIKI_PAGE = 'https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_keywords'

            # Get the wikipage initially
            wiki = requests.get(WIKI_PAGE)
            wikisoup = bs.BeautifulSoup(wiki.content, 'lxml')
            def_soup = wikisoup.find('div', {'class': 'mw-parser-output'})
            defs_list = []
            defs_dict = {}
            old_len = len(json.loads(open(self.config['mtg_keywords_file'], 'r').read()))

            for keyword in def_soup:
                defs_list.append(keyword)

            for i in range(len(defs_list)):
                if defs_list[i].name == 'h3':
                    keyword_name = defs_list[i].text.replace('[edit]','').lower()
                    keyword_def = defs_list[i+2].text
                    defs_dict[keyword_name] = keyword_def

            new_len = len(defs_dict)
            with open(self.config['mtg_keywords_file'], "w") as f:
                f.write(json.dumps(defs_dict))

            final_mage_response = f"Definitions successfully updated. Added {new_len - old_len} keyword definitions. There are a total of {new_len} keywords."
        except:
            old_len = len(json.loads(open(self.config['mtg_keywords_file'], 'r').read()))
            final_mage_response = f"Something went wrong renewing the definitions.  There are currently {old_len} keywords." 

        return final_mage_response


