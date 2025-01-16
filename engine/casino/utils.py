import engine.sql as sql
import logging
import engine.bot as bot
import engine.casino.gamble as gamble


def load_casino_cog(client):
    try:
        client.load_extension('engine.casino.cog')
        logging.info(f'Модуль казино успешно загружен.')
    except Exception as error:
        logging.error(f'Ошибка при попытке загрузки модуля казино. Дополнительная информация: {error}')


def set_game(player, game, reset=True):
    gamble_cog = bot.client.get_cog('Casino')
    game_instance = None
    if game == "slot_machine":
        if reset:
            gamble_cog.gambling_pool[player]['slot_machine'] = None
        game_instance = gamble_cog.gambling_pool[player]['slot_machine'] = gamble.SlotMachine(player)
    elif game == "roulette":
        if reset:
            gamble_cog.gambling_pool[player]['roulette'] = None
        game_instance = gamble_cog.gambling_pool[player]['roulette'] = gamble.Roulette(player)
    elif game == "yahtzee":
        if reset:
            gamble_cog.gambling_pool[player]['yahtzee'] = None
        game_instance = gamble_cog.gambling_pool[player]['yahtzee'] = gamble.Yahtzee(player)
    return game_instance



def get_valid_field(field, field_type="sector"):
    try:
        int_field = int(field)
        if field_type == "sector":
            return int_field if 0 <= int_field <= 36 else False
        elif field_type == "trinary":
            return int_field if 1 <= int_field <= 3 else False
        elif field_type == "sixline":
            return int_field if 1 <= int_field <= 6 else False
    except (ValueError, TypeError):
        return False

def get_valid_bet(bet, lower_limit=1, limit=1):
    try:
        int_bet = int(bet)
        if lower_limit <= int_bet <= limit:
            return int_bet
    except (ValueError, TypeError):
        return False

def is_enough_balance(player, bet, overall_bets=0):
    return sql.get_user_balance(player) >= bet + overall_bets