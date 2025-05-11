import os
import tempfile
import json
import random
import logging
import requests
from datetime import datetime, time, timedelta, timezone
import engine.config as config
import engine.sql as sql


def catch_attempt():
    rand = random.random()
    if rand < config.PROBABILITIES['legendary']:
        amount_of_caught_frogs = random.randint(8, 50)
    elif rand < config.PROBABILITIES['epic']:
        amount_of_caught_frogs = random.choice([5, 6, 7])
    elif rand < config.PROBABILITIES['uncommon']:
        amount_of_caught_frogs = random.choice([3, 4])
    elif rand < config.PROBABILITIES['common']:
        amount_of_caught_frogs = random.choice([1, 2])
    else:
        amount_of_caught_frogs = 0
    return amount_of_caught_frogs


def get_timestamp():
    return int(datetime.now(timezone.utc).timestamp())


def from_timestamp(timestamp, mode="time"):
    pattern = '%d/%m/%Y' if mode == "date" else '%H:%M:%S'
    return datetime.utcfromtimestamp(timestamp).strftime(pattern)


def get_time_object(hour=0, minute=0):
    return time(hour=hour, minute=minute)


def get_short_date(timestamp, previous=False):
    date = datetime.strptime(from_timestamp(timestamp, mode="date"), "%d/%m/%Y")
    if previous:
        first_day_of_current_month = date.replace(day=1)
        date = first_day_of_current_month - timedelta(days=1)
    return date.strftime("%Y-%m")


def get_previous_day(timestamp):
    date = datetime.strptime(from_timestamp(timestamp, mode="date"), "%d/%m/%Y")
    date -= timedelta(days=1)
    return date.strftime("%d/%m/%Y")


def get_month_name(month, case="nominative"):
    months = {
        "01": {"nominative": "январь", "accusative": "января"},
        "02": {"nominative": "февраль", "accusative": "февраля"},
        "03": {"nominative": "март", "accusative": "марта"},
        "04": {"nominative": "апрель", "accusative": "апреля"},
        "05": {"nominative": "май", "accusative": "мая"},
        "06": {"nominative": "июнь", "accusative": "июня"},
        "07": {"nominative": "июль", "accusative": "июля"},
        "08": {"nominative": "август", "accusative": "августа"},
        "09": {"nominative": "сентябрь", "accusative": "сентября"},
        "10": {"nominative": "октябрь", "accusative": "октября"},
        "11": {"nominative": "ноябрь", "accusative": "ноября"},
        "12": {"nominative": "декабрь", "accusative": "декабря"},
    }
    return months[month][case]


def numeral(value, value_type="frogs"):
    def get_numeral(value, singular, few, many):
        if 11 <= value % 100 <= 14:
            return many
        last_digit = value % 10
        if last_digit == 1:
            return singular
        elif 2 <= last_digit <= 4:
            return few
        else:
            return many

    if value_type == "frogs":
        return get_numeral(value, "лягушку", "лягушки", "лягушек")
    elif value_type == "hours":
        return get_numeral(value, "час", "часа", "часов")


def validate(value, check_type):
    if check_type == 'cooldown':
        if value.isdigit():
            return 0 < int(value) <= 24
        return False

    elif check_type in ['price', 'gift', 'quiz', 'tax', 'penalty']:
        if value.isdigit():
            return int(value) > 0
        return False

    elif check_type == 'probabilities':
        parsed_probabilities = {}
        for rarity, probability in value.items():
            if not probability.isdigit():
                return False
            parsed_probability = int(probability)
            if not (1 <= parsed_probability <= 99):
                return False
            parsed_probabilities[rarity] = parsed_probability
        probabilities = list(parsed_probabilities.values())
        for i in range(len(probabilities) - 1):
            if probabilities[i] <= probabilities[i + 1]:
                return False
        return True


def set_price(item=None, price=None, reset=False):
    prices = json_safeload(config.PRICES_JSON)
    if reset:
        for key, default_value in prices['default'].items():
            prices['current'][key] = default_value
    else:
        prices["current"][item] = int(price)
    json_safewrite(config.PRICES_JSON, prices)
    config.PRICES = json_safeload(config.PRICES_JSON)['current']


def set_probabilities(updated_probabilities=None, reset=False):
    probabilities = json_safeload(config.PROBABILITIES_JSON)
    if reset:
        probabilities['current'] = probabilities['default']
    else:
        probabilities['current'] = {key: int(value) / 100 for key, value in updated_probabilities.items()}
    json_safewrite(config.PROBABILITIES_JSON, probabilities)
    config.PROBABILITIES = json_safeload(config.PROBABILITIES_JSON)['current']


def set_cooldown(updated_cooldown=None, reset=False):
    cooldown = json_safeload(config.CATCHING_COOLDOWN_JSON)
    if reset:
        cooldown['current'] = cooldown['default']
    else:
        cooldown['current'] = int(updated_cooldown)
    json_safewrite(config.CATCHING_COOLDOWN_JSON, cooldown)
    config.CATCHING_COOLDOWN = json_safeload(config.CATCHING_COOLDOWN_JSON)['current']


def set_taxation(updated_taxation):
    json_safewrite(config.TAXATION_JSON, updated_taxation)
    config.TAXATION = json_safeload(config.TAXATION_JSON)


def json_safeload(filepath):
    if not os.path.isfile(filepath):
        logging.error(f"Произошла ошибка при попытке открытия файла '{filepath}'! Файл не найден.")
        return
    try:
        with open(filepath, 'r') as jsonfile:
            return json.load(jsonfile)
    except Exception as error:
        logging.error(f"Произошла ошибка '{error}' при попытке открытия файла '{filepath}'! Работа бота невозможна")


def json_safewrite(filepath, data):
    dir_name = os.path.dirname(filepath)
    try:
        with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False) as temp_jsonfile:
            temp_jsonfile_name = temp_jsonfile.name
            json.dump(data, temp_jsonfile, indent=4)
        os.replace(temp_jsonfile_name, filepath)
    except Exception as error:
        logging.error(f"Произошла ошибка '{error}' при попытке записи файла '{filepath}'! Изменения не сохранены.")
        if os.path.exists(temp_jsonfile_name):
            os.remove(temp_jsonfile_name)


def get_random_shop_item(item):
    shop_items = config.SHOP_ITEMS_CACHE
    try:
        return f"{config.SHOP_ITEMS_PATH}/{item}/{random.choice(shop_items[item])}"
    except Exception as error:
        logging.error(f"Произошла ошибка '{error}' при попытке извлечения ссылки на файл с предметом "
                      f"из категории '{item}'! Возможно, проблема в некорректном содержимом файла кэша "
                      f"или его отсутствии.")


def refresh_cache():
    expected_directories = {'animal', 'cite', 'food', 'frog', 'meme', 'soundpad', 'track'}

    directory_tree = {}
    files_count = {}

    for root, directories, files in os.walk(config.SHOP_ITEMS_PATH):
        if root == config.SHOP_ITEMS_PATH:
            for directory_name in directories:
                directory_path = os.path.join(root, directory_name)
                items = os.listdir(directory_path)
                directory_tree[directory_name] = items
                files_count[directory_name] = len(items)
            break
    json_safewrite(config.SHOP_ITEMS_CACHE_JSON, directory_tree)
    config.SHOP_ITEMS_CACHE = json_safeload(config.SHOP_ITEMS_CACHE_JSON)
    if set(files_count.keys()) == expected_directories:
        logging.info(f"Содержимое магазина успешно перекэшировано и записано в файл '{config.SHOP_ITEMS_CACHE_JSON}'")
        files_count_printable = '\n'.join(f"*{key}*: **{value}**" for key, value in files_count.items())
        return files_count_printable
    else:
        logging.error("Ошибка при кэшировании файлов. Проверьте наличие директории shop_items и всех "
                      "необходимых подпапок с содержимым.")


def image_download(url):
    if not url:
        return None, None
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        content_type = response.headers['Content-Type']
        if 'image/jpeg' in content_type:
            extension = '.jpg'
        elif 'image/png' in content_type:
            extension = '.png'
        elif 'image/gif' in content_type:
            extension = '.gif'
        else:
            return None, None
        image_binary_data = response.content
        current_unix_time = get_timestamp()
        image_filename = f'{current_unix_time}{extension}'
        return image_binary_data, image_filename
    except requests.exceptions.RequestException:
        return None, None


def setup_directories():
    directories = ['database', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def reset_database():
    try:
        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)
        sql.create_tables()
        logging.info("База данных была обнулена и инициализирована повторно.")
        return True
    except Exception as error:
        logging.error(f"Ошибка '{error}' при попытке обнуления базы данных.")
