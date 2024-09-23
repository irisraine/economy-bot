# Economy Bot

## Description

Welcome to the Frog Economy Bot for Discord! This bot introduces a fun and engaging economy system to your server, 
allowing members to earn and spend an inner server currency called "frogs". With various commands and features, 
users can enjoy a dynamic and interactive experience.

## Features

- **Earn Frogs**: Participate in activities to earn frogs, the server's unique currency.
- **Shop**: Spend your frogs on a variety of items including songs, soundpads, art, memes, wise quotes, premium roles, and more.
- **Catch Frogs**: Try your luck in the swamp to catch frogs with a certain probability.
- **Transfer Frogs**: Easily transfer frogs to other users.
- **Admin Controls**: Special options for admins to adjust prices and configure settings.

## Commands

- `/shop`: Access the shop to browse and purchase items.
- `/catch`: Attempt to catch a frog in the swamp.
- `/balance`: Check your current frog balance.
- `/transfer` <amount> <user>: Transfer a specified amount of frogs to another user.
- `/admin`: Access special admin options to adjust prices and configure other settings.

## Usage

If you want to use this bot locally, please make sure to specify the necessary environment variables by 
creating a .env file in the project directory. This file should contain DISCORD_BOT_TOKEN, GUILD_ID, 
ADMIN_ID and NEWS_CHANNEL_ID environment variables and their corresponding values.
Here is an example:
```
# Bot token
DISCORD_BOT_TOKEN='your-discord-bot-token-here'
# ID of your server
GUILD_ID = 0000000000000000000
# User ID of server's main admin
ADMIN_ID = 0000000000000000000
# ID of news channel available to bot
NEWS_CHANNEL_ID = 0000000000000000000
```
