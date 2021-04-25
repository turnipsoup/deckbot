# Deckbot

Deckbot is a Discord bot made to access MTG: Arena formatted Decks and run statistics for the caller.

### Running

You will want to have three directories as local bind-mounts to persist storage, as well as modify config and add your bot token:

```
mkdir -p ./{logs,cache}
docker run -d -v $(pwd)/logs:/app/deckbot/logs/ -v $(pwd)/cache:/app/deckbot/cache/ -v $(pwd)/config:/app/deckbot/config/ lel/deckbot
```

### Configurations:
`config.json` will have some values put in for you.

What is the MOST IMPORTANT is `config/bot_token.token`. This is the token from ***your*** discord bot you made for this application. Save it in this file with ***NO*** new lines.

The bot uses `async/await` so if one thread horks up and crashes the bot will reconnect and stay up.
