from src import library, librarian, painter, card
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
    logging.info(f'We are logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('~deckbot'):

        deck = message.content.replace('~deckbot', '')
        deck = [x for x in deck.split("\n") if x != '']
        deck_library = library.Library(deck, config)

        # Initiate global
        hands = []

        # Draw 100000 times
        for i in range(config['iterations']):
            deck_library.shuffle()
            hands.append(deck_library.draw(7))
            deck_library.reset_deck()

        custom_defs = {
            'land': ['Needleverge Pathway', 'Wind-Scarred Crag']
            }

        deck_librarian = librarian.Librarian(hands, deck_library)

        averages, totals = deck_librarian.average_all_lands()

        await message.channel.send(averages)

client.run(discord_api_token)