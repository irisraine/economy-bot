import os
import json
import random
import logging
import engine.config as config


def catch_random_amount_of_frogs():
    random_value = random.random()
    if random_value < config.PROBABILITIES['legendary']:
        return random.randint(7, 45)
    elif random_value < config.PROBABILITIES['rare']:
        return random.choice([5, 6])
    elif random_value < config.PROBABILITIES['uncommon']:
        return random.choice([3, 4])
    elif random_value < config.PROBABILITIES['common']:
        return random.choice([1, 2])
    else:
        return 0

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

def json_safeload(filepath):
    try:
        with open(filepath, 'r') as jsonfile:
            return json.load(jsonfile)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        logging.info(f"Произошла ошибка {error} при попытке открытия файла {filepath}! Работа бота невозможна")

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

