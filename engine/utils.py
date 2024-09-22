import os
import json
import random
import logging
import engine.config as config


def numeral(amount):
    if 11 <= amount % 100 <= 14:
        return "лягушек"
    last_digit = amount % 10
    if last_digit == 1:
        return "лягушку"
    elif 2 <= last_digit <= 4:
        return "лягушки"
    else:
        return "лягушек"

def validate_cooldown(cooldown):
    if cooldown.isdigit():
        return 0 < int(cooldown) < 100
    return False

def validate_price(price):
    if price.isdigit():
        return int(price) > 0
    return False

def validate_probabilities(probabilities):
    parsed_probabilities = {}
    for rarity, value in probabilities.items():
        if not value.isdigit():
            return False
        parsed_value = int(value)
        if not (1 <= parsed_value <= 99):
            return False,
        parsed_probabilities[rarity] = parsed_value
    values = list(parsed_probabilities.values())
    for i in range(len(values) - 1):
        if values[i] <= values[i + 1]:
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
    # try:
    #     with open(config.PRICES_JSON, 'w') as jsonfile:
    #         json.dump(prices, jsonfile, indent=4)
    #     config.PRICES = json_safeload(config.PRICES_JSON)['current']
    # except Exception as error:
    #     logging.info(f"Произошла ошибка {error} при попытке записи файла {config.PRICES_JSON}! Изменения не сохранены!")

def set_probabilities(updated_probabilities=None, reset=False):
    probabilities = json_safeload(config.PROBABILITIES_JSON)
    if reset:
        probabilities['current'] = probabilities['default']
    else:
        probabilities['current'] = {key: int(value) / 100 for key, value in updated_probabilities.items()}
    json_safewrite(config.PROBABILITIES_JSON, probabilities)
    config.PROBABILITIES = json_safeload(config.PROBABILITIES_JSON)['current']

    # try:
    #     with open(config.PROBABILITIES_JSON, 'w') as jsonfile:
    #         json.dump(probabilities, jsonfile, indent=4)
    #     config.PROBABILITIES = json_safeload(config.PROBABILITIES_JSON)['current']
    # except Exception as error:
    #     logging.info(f"Произошла ошибка {error} при попытке записи файла {config.PROBABILITIES_JSON}! Изменения не сохранены!")

def set_cooldown(updated_cooldown=None, reset=False):
    cooldown = json_safeload(config.CATCHING_COOLDOWN_JSON)
    if reset:
        cooldown['current'] = cooldown['default']
    else:
        cooldown['current'] = int(updated_cooldown)
    json_safewrite(config.CATCHING_COOLDOWN_JSON, cooldown)
    config.CATCHING_COOLDOWN = json_safeload(config.CATCHING_COOLDOWN_JSON)['current']

    # try:
    #     with open(config.CATCHING_COOLDOWN, 'w') as jsonfile:
    #         json.dump(cooldown, jsonfile, indent=4)
    #     config.CATCHING_COOLDOWN = json_safeload(config.CATCHING_COOLDOWN)['current']
    # except Exception as error:
    #     logging.info(f"Произошла ошибка {error} при попытке записи файла {config.CATCHING_COOLDOWN}! Изменения не сохранены!")

def json_safeload(filepath):
    try:
        with open(filepath, 'r') as jsonfile:
            return json.load(jsonfile)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        logging.info(f"Произошла ошибка {error} при попытке открытия файла {filepath}! Работа бота невозможна")

def json_safewrite(filepath, data):
    try:
        with open(filepath, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)
    except Exception as error:
        logging.info(
            f"Произошла ошибка {error} при попытке записи файла {filepath}! Изменения не сохранены!")

def get_random_shop_item_filepath(item):
    shop_items = json_safeload(config.SHOP_ITEMS_CACHE)
    return f"{config.SHOP_ITEMS_PATH}/{item}/{random.choice(shop_items[item])}"

def refresh_cache():
    directory_tree = {}
    files_count = {}

    for root, dirs, files in os.walk(config.SHOP_ITEMS_PATH):
        if root == config.SHOP_ITEMS_PATH:
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                items = os.listdir(dir_path)
                directory_tree[dir_name] = items
                files_count[dir_name] = len(items)
            break
    try:
        with open(config.SHOP_ITEMS_CACHE, 'w') as shop_contents_cache:
            json.dump(directory_tree, shop_contents_cache, indent=2)
        files_count_printable = '\n'.join(f"*{key}*: **{value}**" for key, value in files_count.items())
        logging.info(f"Содержимое магазина успешно перекэшировано и записано в файл {config.SHOP_ITEMS_CACHE}")
        return files_count_printable
    except IOError as error:
        logging.info(f"При кэшировании медиафайлов магазина произошла ошибка: {error}")

