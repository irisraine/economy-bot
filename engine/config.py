import os
from dotenv import load_dotenv
import engine.utils as utils


load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
ADMIN_ID = int(os.getenv('ADMIN_ID'))
NEWS_CHANNEL_ID =int(os.getenv('NEWS_CHANNEL_ID'))
PREMIUM_ROLE_ID =int(os.getenv('PREMIUM_ROLE_ID'))

BASIC_COLOR_CODE = (8, 117, 30)
FROG_EMOJI = "<:1frg:1286272480083836970>"

SEPARATOR = "assets/separator.png"
BALANCE_IMAGE = "assets/balance.png"
BANK_BALANCE_IMAGE = "assets/bank_balance.png"
ALL_USERS_BALANCES_IMAGE = "assets/all_users_balances.png"

SHOP_ENTRANCE_IMAGE = "assets/shop_entrance.png"
SHOP_COUNTER_IMAGE = "assets/shop_counter.png"

SET_PRICE_IMAGE = "assets/set_price.png"
SET_PROBABILITIES_IMAGE = "assets/set_probabilities.png"

COOLDOWN_IMAGE = "assets/cooldown.png"

CATCH_FAULT_IMAGE = "assets/catch_fault.png"
CATCH_COMMON_IMAGE = "assets/catch_common.png"
CATCH_UNCOMMON_IMAGE = "assets/catch_uncommon.png"
CATCH_RARE_IMAGE = "assets/catch_rare.png"
CATCH_LEGENDARY_IMAGE = "assets/catch_legendary.png"

TRANSFER_IMAGE = "assets/transfer.png"
TRANSFER_SUCCESS_IMAGE = "assets/transfer_successful.png"
TRANSFER_DENIED_IMAGE = "assets/transfer_denied.png"
TRANSFER_FAILED_TO_SELF_IMAGE = "assets/transfer_to_self.png"
TRANSFER_FAILED_TO_BOT_IMAGE = "assets/transfer_to_bot.png"

SHOP_ITEMS_PATH = "shop_items"
SHOP_ITEMS_CACHE = "settings/cache.json"

ADMIN_PANEL_IMAGE = "assets/admin.png"

SHOP_ITEMS_SERVICES = {
    "drawing": "assets/drawing.png",
    "rain": "assets/rain.png",
    "event": "assets/event.png",
    "role": "assets/role.png",
    "band": "assets/band.png",
}

CATCHING_COOLDOWN_JSON = "settings/cooldown.json"
CATCHING_COOLDOWN = utils.json_safeload(CATCHING_COOLDOWN_JSON)['current']
PRICES_JSON = "settings/prices.json"
PRICES = utils.json_safeload(PRICES_JSON)['current']
PROBABILITIES_JSON = "settings/probabilities.json"
PROBABILITIES = utils.json_safeload(PROBABILITIES_JSON)['current']
