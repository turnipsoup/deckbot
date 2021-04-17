from src import library, librarian, painter, card, mage
import sqlite3, os, logging, json, discord

# Load config file
config_dir = './config'
config = json.loads(open(f"{config_dir}/config.json", "r").read())
discord_api_token = open(f'{config_dir}/bot_token.token').read()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s|%(levelname)s|%(message)s"
    )



# Initiate discord client
client = discord.Client()

@client.event
async def on_ready():
    logging.info(f'We are logged in as {client.user} to {client.guilds}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('~deckbot'):

        # Handle requests for land averages
        if message.content.split()[1] == 'landavg':
            mage_response = mage.Mage(message.content, config).get_land_average()
            

        await message.channel.send(mage_response)

client.run(discord_api_token)