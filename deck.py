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

    if message.content.startswith(config['call_name']):

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
            mage_response += deck_mage.get_specific_average()

        await message.channel.send(mage_response)

client.run(discord_api_token)