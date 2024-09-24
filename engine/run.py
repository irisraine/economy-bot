from engine.bot import client
from engine.logger import init_logger
import engine.config as config


def run_discord_bot():
    init_logger()
    client.run(config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    run_discord_bot()
