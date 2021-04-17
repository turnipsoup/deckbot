
import requests, json, sqlite3, logging, string

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s|%(levelname)s|%(message)s"
    )


# Define some globals
api_endpoint = 'https://api.magicthegathering.io'
api_version = 'v1'


class Card:

    def __init__(self, name='Blank'):
        self.name = name

        # Clean name for use as a file name, or whatever
        self.clean_name = self.name.translate(str.maketrans('', '', string.punctuation)).replace(" ", "_")

        self.cache_dir = './cache'

        

        self.cache_card()
        self.get_local_info()
        self.fill_vals()

    def get_info(self):
        '''
        Fetch the card info from magicthegathering.io, returns a dict.
        '''
        card_endpoint = f'{api_endpoint}/{api_version}/cards?name={self.name}'
        
        try:
            r = requests.get(card_endpoint).json()['cards'][0]

            self.card_info = r

            logging.info(f'Card {self.name} fetched from the API.')
        except:
            logging.error(f'Failed to fetch card {self.name} from {card_endpoint}')

    def fill_vals(self, cache_dict={}):
        '''
        Converts values from the self.card_info dict
        to inherit values of the class.
        '''

        # Get an array of values for the mana cost. Unless it doesnt have one
        # (like a land). In that case, set to None value.
        try:
            self.mana_cost = [ x for x in self.card_info['manaCost'].replace('{', '').replace('}', '')]
        except:
            self.mana_cost = None
        
        # Colors or no colors
        try:
            self.colors = self.card_info['colors']
        except:
            self.colors = ['Colorless']

        self.cmc = self.card_info['cmc']
        self.color_identity = self.card_info['colorIdentity']
        self.types = self.card_info['types']
        self.rarity = self.card_info['rarity']
        self.set = self.card_info['set']
        self.set_name = self.card_info['setName']
        self.text = self.card_info['text']

        # Not every card has these
        try:
            self.power = self.card_info['power']
        except:
            self.power = None

        try:
            self.toughness = self.card_info['toughness']
        except:
            self.toughness = None

        try:
            self.sub_types = self.card_info['subtypes']
        except:
            self.sub_types = None

    def cache_card(self):
        '''
        Caches card if it does not exist.

        Will load a sqlite3 db that contains the card name, file path
        of the stored card. The card will be the raw JSON returned from the API
        stored in the cache directory.

        Returns True if card was cached. Returns False if it exited.
        '''
        db = f'{self.cache_dir}/cards.db'
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        try:
            cursor.execute('''CREATE TABLE cards (name TEXT, path TEXT)''')
            logging.info(f'Created database {db}')
        except:
            logging.debug(f'Database {db} already exists, loading!')

        select = f"""SELECT * FROM cards WHERE name = '{self.clean_name}'"""

        if len(cursor.execute(f"""SELECT * FROM cards WHERE name LIKE '%{self.clean_name}%'""").fetchall()) > 0:
            logging.info(f'Card {self.name} is already cached!')
            connection.close()
            return False
        
        cursor.execute('INSERT INTO cards(name, path) VALUES(?,?)', (self.clean_name, f'{self.cache_dir}/{self.clean_name}.json'))
        cursor.execute('COMMIT')

        self.get_info()
        self.write_card()

        logging.info(f'Card {self.name} has been cached')
        connection.close()
        return True

    def write_card(self):
        with open(f'{self.cache_dir}/{self.clean_name}.json', 'w') as f:
            f.write(json.dumps(self.card_info))
            f.close()

    def get_local_info(self):

        card_data =  json.loads(open(f'{self.cache_dir}/{self.clean_name}.json', 'r').read())
        self.card_info = card_data
        self.fill_vals()
        
        
            
        



            

