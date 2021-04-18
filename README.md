# Deckbot

Deckbot is a Discord bot made to access MTG: Arena formatted Decks and run statistics for the caller.

### Installing
You will want to be using a Python3 Virtualenv

Linux:
```
apt install python3-venv
# or
dnf install python3-venv
```

Mac:
```
brew install python3-venv
```

Next, you will want to clone the directory, `cd` into it, and then make your venv directory.

```
git clone git@github.com:turnipsoup/deckbot.git
cd deckbot
mkdir env
python3 -m venv env
source env/bin/active
pip install -r requirements.txt
```

### Running

Currently, its basic af...
```
python deck.py
```

### Configurations:
`config.json` will have some values put in for you.

What is the MOST IMPORTANT is `config/bot_token.token`. This is the token from ***your*** discord bot you made for this application. Save it in this file with ***NO*** new lines.

The bot uses `async/await` so if one thread horks up and crashes the bot will reconnect and stay up.
