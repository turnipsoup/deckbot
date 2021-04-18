import requests, json, sqlite3, string, os
from . import setup_logger

logger = setup_logger.logger

# Define some globals
api_endpoint = 'https://api.magicthegathering.io'
api_version = 'v1'


class Card:
    def __init__(self, config, name='Forest'):
        self.name = name

        # Clean name for use as a file name, or whatever
        self.clean_name = self.name.translate(str.maketrans('', '', string.punctuation)).replace(" ", "_")

        self.cache_dir = config['cache_dir']

        

        self.cache_card() # Cache card if it is not cached
        self.get_local_info() # Load locally cached chard
        self.fill_vals() # Unmarshal card into inherit values for the class

    def get_info(self):
        '''
        Fetch the card info from magicthegathering.io, returns a dict.
        '''
        card_endpoint = f'{api_endpoint}/{api_version}/cards?name={self.name}'
        
        try:
            r = requests.get(card_endpoint).json()['cards'][0]

            self.card_info = r

            logger.info(f'Card {self.name} fetched from the API.')
        except:
            logger.error(f'Failed to fetch card {self.name} from {card_endpoint}')

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

        try:
            self.cmc = self.card_info['cmc']
        except:
            self.cmc = None

        try:
            self.color_identity = self.card_info['colorIdentity']
        except:
            self.color_identity = None

        try:
            self.types = self.card_info['types']
        except:
            self.color_identity = ['Typeless']

        try:
            self.rarity = self.card_info['rarity']
        except:
            self.rarity = None

        try:
            self.set = self.card_info['set']
        except:
            self.set = None

        try:
            self.set_name = self.card_info['setName']
        except:
            self.set_name = None

        try:
            self.text = self.card_info['text']
        except:
            self.text = None
            
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
        if os.path.isdir(self.cache_dir):
            pass
        else:
            os.mkdir(self.cache_dir)

        db = f'{self.cache_dir}/cards.db'
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        try:
            cursor.execute('''CREATE TABLE cards (name TEXT, path TEXT)''')
            logger.info(f'Created database {db}')
        except:
            logger.debug(f'Database {db} already exists, loading!')

        select = f"""SELECT * FROM cards WHERE name = '{self.clean_name}'"""

        if len(cursor.execute(f"""SELECT * FROM cards WHERE name LIKE '%{self.clean_name}%'""").fetchall()) > 0:
            logging.info(f'Card {self.name} loaded from cache')
            connection.close()
            return False

        self.get_info()
        self.write_card()

        cursor.execute('INSERT INTO cards(name, path) VALUES(?,?)', (self.clean_name, f'{self.cache_dir}/{self.clean_name}.json'))
        cursor.execute('COMMIT')

        logger.info(f'Card {self.name} has been cached')
        connection.close()
        return True

    def write_card(self):
        '''
        Write card to cache directory
        '''
        with open(f'{self.cache_dir}/{self.clean_name}.json', 'w') as f:
            f.write(json.dumps(self.card_info))
            f.close()

    def get_local_info(self):
        '''
        Load card from cache directory
        '''
        card_data =  json.loads(open(f'{self.cache_dir}/{self.clean_name}.json', 'r').read())
        self.card_info = card_data
        
        
            
        



            

