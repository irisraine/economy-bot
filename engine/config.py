import os
from dotenv import load_dotenv
import engine.utils as utils


load_dotenv()

LOGGING_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(levelname)s] : %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'logs/economy-bot.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
ADMIN_ID = int(os.getenv('ADMIN_ID'))
NEWS_CHANNEL_ID = int(os.getenv('NEWS_CHANNEL_ID'))
ECONOMY_BOT_MAIN_CHANNEL = int(os.getenv('ECONOMY_BOT_MAIN_CHANNEL'))

PREMIUM_ROLE = {
    "lite": int(os.getenv('PREMIUM_ROLE_LITE_ID')),
    "basic": int(os.getenv('PREMIUM_ROLE_ID')),
    "max": int(os.getenv('PREMIUM_ROLE_MAX_ID'))
}

QUIZ_PARTICIPANT_ID = int(os.getenv('QUIZ_PARTICIPANT_ID'))

DATABASE_PATH = "database/vault.db"

BASIC_COLOR_CODE = (97, 194, 0)
ERROR_COLOR_CODE = (255, 0, 0)

CATCHING_COOLDOWN_JSON = "settings/cooldown.json"
CATCHING_COOLDOWN = utils.json_safeload(CATCHING_COOLDOWN_JSON)['current']
PRICES_JSON = "settings/prices.json"
PRICES = utils.json_safeload(PRICES_JSON)['current']
PROBABILITIES_JSON = "settings/probabilities.json"
PROBABILITIES = utils.json_safeload(PROBABILITIES_JSON)['current']
TAXATION_JSON = "settings/taxation.json"
TAXATION = utils.json_safeload(TAXATION_JSON)

PREMIUM_ROLE_DURATION = 2592000

QUIZ_ROUND_TIME = 60
QUIZ_ACTIVE_TIME = 1800

TAXES_COLLECTION_AND_ENCASHMENT_TIME = utils.get_time_object(
    hour=0,
    minute=30
)

FROG_EMOJI = "<:1fb:1227748132868194346>"

SEPARATOR = "assets/separator.png"
SUCCESS_OPERATION_IMAGE = "assets/success_operation.jpg"
ERROR_IMAGE = "assets/error.jpg"
ERROR_SHOP_IMAGE = "assets/error_shop.jpg"

SHOP_ENTRANCE_IMAGE = "assets/shop_entrance.jpg"
SHOP_COUNTER_IMAGE = "assets/shop_counter.jpg"

SHOP_ITEMS_PATH = "shop_items"
SHOP_ITEMS_CACHE_JSON = "settings/cache.json"
SHOP_ITEMS_CACHE = utils.json_safeload(SHOP_ITEMS_CACHE_JSON)
SHOP_ITEMS_SERVICES = {
    "drawing": "assets/drawing.jpg",
    "rain": "assets/rain.jpg",
    "role_lite": "assets/role_lite.jpg",
    "role": "assets/role.jpg",
    "band": "assets/band.jpg",
}

BALANCE_IMAGE = "assets/balance.jpg"

CATCH_FAULT_IMAGE = "assets/catch_fault.jpg"
CATCH_COMMON_IMAGE = "assets/catch_common.jpg"
CATCH_UNCOMMON_IMAGE = "assets/catch_uncommon.jpg"
CATCH_EPIC_IMAGE = "assets/catch_epic.jpg"
CATCH_LEGENDARY_IMAGES = {
    1: "assets/catch_legendary_tier_1.jpg",
    2: "assets/catch_legendary_tier_2.jpg",
    3: "assets/catch_legendary_tier_3.jpg",
    4: "assets/catch_legendary_tier_4.jpg",
    5: "assets/catch_legendary_tier_5.jpg",
    6: "assets/catch_legendary_tier_6.jpg",
    7: "assets/catch_legendary_tier_7.jpg",
    8: "assets/catch_legendary_tier_8.jpg",
    9: "assets/catch_legendary_tier_9.jpg",
    10: "assets/catch_legendary_tier_10.jpg"
}

COOLDOWN_IMAGE = "assets/cooldown.jpg"

TRANSFER_IMAGE = "assets/transfer.jpg"
TRANSFER_SUCCESS_IMAGE = "assets/transfer_successful.jpg"
TRANSFER_DENIED_IMAGE = "assets/transfer_denied.jpg"
TRANSFER_FAILED_TO_SELF_IMAGE = "assets/transfer_to_self.jpg"
TRANSFER_FAILED_TO_BOT_IMAGE = "assets/transfer_to_bot.jpg"

SETTINGS_MENU_IMAGE = "assets/settings_menu.jpg"

CACHING_IMAGE = "assets/caching.jpg"
CACHING_SUCCESSFUL_IMAGE = "assets/caching_successful.jpg"

SET_PRICE_IMAGE = "assets/set_price.jpg"
SET_PROBABILITIES_IMAGE = "assets/set_probabilities.jpg"

BANK_BALANCE_IMAGE = "assets/bank_balance.jpg"
CASINO_BALANCE_IMAGE = "assets/casino_balance.jpg"
ALL_USERS_BALANCES_IMAGE = "assets/all_users_balances.jpg"

TAXES_COLLECTION_IMAGE = "assets/taxes_collection.jpg"
TAXES_ON_IMAGE = "assets/taxes_on.jpg"
TAXES_OFF_IMAGE = "assets/taxes_off.jpg"
ENCASHMENT_IMAGE = "assets/encashment.jpg"

GIFT_IMAGE = "assets/gift.jpg"
GIFT_SUCCESS_IMAGE = "assets/gift_successful.jpg"

CONFISCATION_IMAGE = "assets/confiscation.jpg"
CONFISCATION_SUCCESS_IMAGE = "assets/confiscation_successful.jpg"

ROLE_LISTING_IMAGE = "assets/role_listing.jpg"
ROLE_REMOVAL_IMAGE = "assets/role_removal.jpg"
ROLE_NOTHING_TO_REMOVE_IMAGE = "assets/role_nothing_to_remove.jpg"

NEWS_POST_IMAGE = "assets/post_news.jpg"

QUIZ_IMAGE = "assets/quiz.jpg"
QUIZ_TIME_UP = "assets/quiz_time_up.jpg"
QUIZ_PRIZE_BASIC = "assets/quiz_prize_basic.jpg"
QUIZ_PRIZE_SPECIAL = "assets/quiz_prize_special.jpg"
QUIZ_PRIZE_FORBIDDEN = "assets/quiz_prize_forbidden.jpg"

USER_REMOVED_IMAGE = "assets/user_removed.jpg"
