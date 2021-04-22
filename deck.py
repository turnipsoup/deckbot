from src import library, librarian, painter, card, mage, setup_logger
import sqlite3, os, logging, json, discord, sys

# Instantiate logger
logger = setup_logger.logger

# Log version number
with open("VERSION") as f:
    logger.info(f"Starting Deckbot version {f.read()}")

# Load config file
config_dir = './config'
config = json.loads(open(f"{config_dir}/config.json", "r").read())
logger.info("Successfully loaded config")
discord_api_token = open(f'{config_dir}/bot_token.token').read()
logger.info("Successfully loaded Discord API Token")

# Define known actions
known_actions = [
    'fullavg', 'landavg', 'nonlandavg', 'cardinfo', 'define'
]

# Initiate discord client
client = discord.Client()

@client.event
async def on_ready():
    logger.info(f'We are logged in as {client.user} to {client.guilds}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(config['call_name']):


        try:

            logger.info(f'Request {message.content.split()[1]} initiated by {message.author}')
            logger.debug(f'Request: {message.content}')

            # Handle requests for land averages
            if message.content.split()[1] == 'landavg':
                deck_mage = mage.Mage(message.content, config)
                mage_response = deck_mage.get_land_average()

            if message.content.split()[1] == 'nonlandavg':
                deck_mage = mage.Mage(message.content, config)
                mage_response = deck_mage.get_specific_average()

            if message.content.split()[1] == 'fullavg':
                deck_mage = mage.Mage(message.content, config)
                mage_response = deck_mage.get_land_average() + '\n\n'
                mage_response += deck_mage.get_specific_average() + '\n\n'
                mage_response += deck_mage.get_average_hand_cmc() + '\n\n'
                mage_response += deck_mage.get_sample_hands()

            if message.content.split()[1] == 'cardinfo':
                deck_mage = mage.Mage(message.content, config)
                mage_response = deck_mage.get_card_info()
            
            if message.content.split()[1] == 'define':
                deck_mage = mage.Mage(message.content, config)
                mage_response = deck_mage.get_keyword_definition()

        except: # Throw the error into the logs and carry on
            logger.exception("Error caught processing the user request!")
            logger.error(f"Failed message: {message.content}")
            mage_response = f'Error processing request, I am sorry!'

                    
        

        await message.channel.send(mage_response)

client.run(discord_api_token)