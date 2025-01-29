import logging.config
import engine.config as config
from engine.bot import client
from engine.utils import setup_directories
from engine.casino.utils import load_casino_cog


def run_discord_bot():
    setup_directories()
    logging.config.dictConfig(config.LOGGING_SETTINGS)
    load_casino_cog(client)
    client.run(config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    run_discord_bot()
