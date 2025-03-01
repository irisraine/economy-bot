import engine.sql as sql
import logging
import engine.bot as bot
import engine.casino.gamble as gamble


def load_casino_cog(client):
    try:
        client.load_extension('engine.casino.cog')
        logging.info("Модуль казино успешно загружен.")
    except Exception as error:
        logging.error(f"Ошибка при попытке загрузки модуля казино. Дополнительная информация: {error}")


def set_game(player, game, reset=False):
    gamble_cog = bot.client.get_cog('Casino')
    if reset:
        gamble_cog.gambling_pool[player][game] = None
        return
    game_instance = None
    if game == "slot_machine":
        game_instance = gamble_cog.gambling_pool[player][game] = gamble.SlotMachine(player)
    elif game == "roulette":
        game_instance = gamble_cog.gambling_pool[player][game] = gamble.Roulette(player)
    elif game == "yahtzee":
        game_instance = gamble_cog.gambling_pool[player][game] = gamble.Yahtzee(player)
    return game_instance


def roulette_bet_value_transcript(bet_category, value):
    if bet_category == "straight":
        return f"сектор {value}"
    elif bet_category == "color":
        return "красное" if value == "red" else "черное"
    elif bet_category == "even_odd":
        return "четное" if value == "even" else "нечетное"
    elif bet_category == "high_low":
        return "высокие" if value == "high" else "низкие"
    elif bet_category == "dozen":
        return f"{value}-ю дюжину"
    elif bet_category == "row":
        return f"{value}-й ряд"
    elif bet_category == "sixline":
        return f"{value}-й сикслайн"


def roulette_valid_field(field, field_type="straight"):
    try:
        int_field = int(field)
        if field_type == "straight":
            return int_field if 0 <= int_field <= 36 else False
        elif field_type == "trinary":
            return int_field if 1 <= int_field <= 3 else False
        elif field_type == "sixline":
            return int_field if 1 <= int_field <= 6 else False
    except (ValueError, TypeError):
        return False


def valid_bet(bet, lower_limit, upper_limit):
    try:
        int_bet = int(bet)
        if lower_limit <= int_bet <= upper_limit:
            return int_bet
    except (ValueError, TypeError):
        return False


def is_enough_balance(player, bet, overall_bets=0):
    return sql.get_user_balance(player) >= bet + overall_bets
