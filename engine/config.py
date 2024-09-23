import os
from dotenv import load_dotenv
import engine.utils as utils


load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
ADMIN_ID = int(os.getenv('ADMIN_ID'))
NEWS_CHANNEL_ID = int(os.getenv('NEWS_CHANNEL_ID'))
PREMIUM_ROLE_ID = int(os.getenv('PREMIUM_ROLE_ID'))

BASIC_COLOR_CODE = (8, 117, 30)
FROG_EMOJI = "<:1frg:1286272480083836970>"

SEPARATOR = "assets/separator.png"
BALANCE_IMAGE = "assets/balance.jpg"
BANK_BALANCE_IMAGE = "assets/bank_balance.jpg"
ALL_USERS_BALANCES_IMAGE = "assets/all_users_balances.jpg"

SHOP_ENTRANCE_IMAGE = "assets/shop_entrance.jpg"
SHOP_COUNTER_IMAGE = "assets/shop_counter.jpg"

SET_PRICE_IMAGE = "assets/set_price.jpg"
SET_PROBABILITIES_IMAGE = "assets/set_probabilities.jpg"

COOLDOWN_IMAGE = "assets/cooldown.jpg"

CATCH_FAULT_IMAGE = "assets/catch_fault.jpg"
CATCH_COMMON_IMAGE = "assets/catch_common.jpg"
CATCH_UNCOMMON_IMAGE = "assets/catch_uncommon.jpg"
CATCH_EPIC_IMAGE = "assets/catch_epic.jpg"
CATCH_LEGENDARY_IMAGE = "assets/catch_legendary.jpg"

TRANSFER_IMAGE = "assets/transfer.jpg"
TRANSFER_SUCCESS_IMAGE = "assets/transfer_successful.jpg"
TRANSFER_DENIED_IMAGE = "assets/transfer_denied.jpg"
TRANSFER_FAILED_TO_SELF_IMAGE = "assets/transfer_to_self.jpg"
TRANSFER_FAILED_TO_BOT_IMAGE = "assets/transfer_to_bot.jpg"

GIFT_IMAGE = "assets/gift.jpg"
GIFT_SUCCESS_IMAGE = "assets/gift_successful.jpg"

SHOP_ITEMS_PATH = "shop_items"
SHOP_ITEMS_CACHE = "settings/cache.json"

ADMIN_MENU_IMAGE = "assets/admin_menu.jpg"

NEWS_POST_IMAGE = "assets/post_news.jpg"

CACHING_SUCCESSFUL_IMAGE = "assets/caching_successful.jpg"

SHOP_ITEMS_SERVICES = {
    "drawing": "assets/drawing.jpg",
    "rain": "assets/rain.jpg",
    "event": "assets/event.jpg",
    "role": "assets/role.jpg",
    "band": "assets/band.jpg",
}

ERROR_IMAGE = "assets/error.jpg"
SUCCESS_OPERATION_IMAGE = "assets/success_operation.jpg"

CATCHING_COOLDOWN_JSON = "settings/cooldown.json"
CATCHING_COOLDOWN = utils.json_safeload(CATCHING_COOLDOWN_JSON)['current']
PRICES_JSON = "settings/prices.json"
PRICES = utils.json_safeload(PRICES_JSON)['current']
PROBABILITIES_JSON = "settings/probabilities.json"
PROBABILITIES = utils.json_safeload(PROBABILITIES_JSON)['current']
