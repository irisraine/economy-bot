import os
import logging.config
import engine.config as config
from engine.bot import client
from engine.casino.utils import load_casino_cog


def run_discord_bot():
    if not os.path.exists('database'):
        os.makedirs('database')
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.config.dictConfig(config.LOGGING_SETTINGS)
    load_casino_cog(client)
    client.run(config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    run_discord_bot()
