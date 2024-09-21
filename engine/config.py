import os
from dotenv import load_dotenv
import engine.utils as utils


load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

CATCHING_COOLDOWN = 10

BASIC_COLOR_CODE = (8, 117, 30)

SEPARATOR = "assets/separator.png"
BALANCE_IMAGE = "assets/balance.png"

SHOP_ENTRANCE_IMAGE = "assets/shop_entrance.png"
SHOP_COUNTER_IMAGE = "assets/shop_counter.png"

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

PRICES = utils.json_safeload("settings/prices.json")['current']
PROBABILITIES = utils.json_safeload("settings/probabilities.json")['current']
