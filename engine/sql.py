import sqlite3
import logging
import engine.config as config


def catch_sql_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            logging.error(f'Ошибка доступа к базе данных! Дополнительная информация: {e}')
    return wrapper


@catch_sql_exceptions
def create_tables():
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS user_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_discord_id INTEGER NOT NULL,
            user_discord_name TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0,
            last_catching_time INTEGER NOT NULL DEFAULT 0
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS bank_balance (
            balance INTEGER NOT NULL DEFAULT 0
            )""")
        cursor.execute("""INSERT INTO bank_balance (balance)
            SELECT 0
            WHERE NOT EXISTS (SELECT 1 FROM bank_balance
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS casino_balance (
            overall_bets INTEGER NOT NULL DEFAULT 0,
            payouts INTEGER NOT NULL DEFAULT 0
            )""")
        cursor.execute("""INSERT INTO casino_balance (overall_bets, payouts)
            SELECT 0, 0
            WHERE NOT EXISTS (SELECT 1 FROM casino_balance
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS encashment (
            amount_to_withdrawal INTEGER NOT NULL DEFAULT 0
            )""")
        cursor.execute("""INSERT INTO encashment (amount_to_withdrawal)
            SELECT 0
            WHERE NOT EXISTS (SELECT 1 FROM encashment
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS quiz_statistics (
            total_quizzes_held INTEGER NOT NULL DEFAULT 0,
            correct_answers INTEGER NOT NULL DEFAULT 0,
            overall_prizes_amount INTEGER NOT NULL DEFAULT 0
            )""")
        cursor.execute("""INSERT INTO quiz_statistics (total_quizzes_held, correct_answers, overall_prizes_amount)
            SELECT 0, 0, 0
            WHERE NOT EXISTS (SELECT 1 FROM quiz_statistics
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS premium_role_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_discord_id INTEGER NOT NULL,
            user_discord_name TEXT NOT NULL,
            role_tier TEXT NOT NULL,
            expiration_time INTEGER NOT NULL
            )""")


@catch_sql_exceptions
def get_user_balance(user):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT balance FROM user_balances WHERE user_discord_id = ?",
                       (user.id,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute("INSERT INTO user_balances (user_discord_id, user_discord_name) VALUES (?, ?)",
                           (user.id, user.name))
            return 0
        return row[0]


@catch_sql_exceptions
def get_all_users_balances():
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT user_discord_id, user_discord_name, balance FROM user_balances "
                       "WHERE balance > 0 ORDER BY balance DESC")
        return cursor.fetchall()


@catch_sql_exceptions
def get_last_catching_time(user):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT last_catching_time FROM user_balances WHERE user_discord_id = ?",
                       (user.id,))
        return cursor.fetchone()[0]


@catch_sql_exceptions
def set_user_balance(user, amount):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT balance, user_discord_name FROM user_balances WHERE user_discord_id = ?",
                       (user.id,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute("INSERT INTO user_balances (user_discord_id, user_discord_name) VALUES (?, ?)",
                           (user.id, user.name))
        current_user_discord_name = row[1]
        if current_user_discord_name != user.name:
            cursor.execute("UPDATE user_balances SET user_discord_name = ? WHERE user_discord_id = ?",
                           (user.name, user.id))
        cursor.execute("UPDATE user_balances SET balance = balance + ? WHERE user_discord_id = ?",
                       (amount, user.id,))


@catch_sql_exceptions
def set_last_catching_time(user, current_time):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("UPDATE user_balances SET last_catching_time = ? WHERE user_discord_id = ?",
                       (current_time, user.id,))


@catch_sql_exceptions
def get_bank_balance():
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT balance FROM bank_balance")
        return cursor.fetchone()[0]


@catch_sql_exceptions
def set_bank_balance(amount):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("UPDATE bank_balance SET balance = balance + ?",
                       (amount,))
    set_encashment_amount(amount=amount)


@catch_sql_exceptions
def get_casino_balance():
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT overall_bets, payouts FROM casino_balance")
        return cursor.fetchone()


@catch_sql_exceptions
def set_casino_balance(bet=0, payout=0):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        if bet:
            cursor.execute("UPDATE casino_balance SET overall_bets = overall_bets + ?",
                           (bet,))
        if payout:
            cursor.execute("UPDATE casino_balance SET payouts = payouts + ?",
                           (payout,))
    set_encashment_amount(amount=max(bet - payout, 0))


@catch_sql_exceptions
def get_encashment_amount():
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT amount_to_withdrawal FROM encashment")
        return cursor.fetchone()[0]


@catch_sql_exceptions
def set_encashment_amount(amount=0, reset=False):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        if reset:
            cursor.execute("UPDATE encashment SET amount_to_withdrawal = 0")
        else:
            cursor.execute("UPDATE encashment SET amount_to_withdrawal = amount_to_withdrawal + ?",
                           (amount,))


@catch_sql_exceptions
def set_quiz_statistics(add_quiz=False, prize_amount=0):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        if add_quiz:
            cursor.execute("UPDATE quiz_statistics SET total_quizzes_held = total_quizzes_held + 1")
        if prize_amount:
            cursor.execute("UPDATE quiz_statistics SET correct_answers = correct_answers + 1")
            cursor.execute("UPDATE quiz_statistics SET overall_prizes_amount = overall_prizes_amount + ?",
                           (prize_amount,))


@catch_sql_exceptions
def get_quiz_statistics():
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT total_quizzes_held, correct_answers, overall_prizes_amount FROM quiz_statistics")
        return cursor.fetchone()


@catch_sql_exceptions
def add_premium_role_user(user, expiration_time, role_tier="basic"):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT COUNT(*) FROM premium_role_users WHERE user_discord_id = ? AND role_tier = ?",
                       (user.id, role_tier))
        user_exists = cursor.fetchone()[0]
        if user_exists:
            cursor.execute("UPDATE premium_role_users "
                           "SET user_discord_name = ?, expiration_time = ? WHERE user_discord_id = ? AND role_tier = ?",
                           (user.name, expiration_time, user.id, role_tier))
        else:
            cursor.execute("INSERT INTO premium_role_users "
                           "(user_discord_id, user_discord_name, role_tier, expiration_time) VALUES (?, ?, ?, ?)",
                           (user.id, user.name, role_tier, expiration_time))


@catch_sql_exceptions
def get_all_premium_role_users(role_tier="basic"):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT user_discord_name, expiration_time FROM premium_role_users WHERE role_tier = ?",
                       (role_tier, ))
        return cursor.fetchall()


@catch_sql_exceptions
def remove_expired_premium_role_users(current_time, role_tier="basic"):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT user_discord_id FROM premium_role_users WHERE expiration_time < ? AND role_tier = ?",
                       (current_time, role_tier))
        expired_premium_role_users_ids = cursor.fetchall()
        if expired_premium_role_users_ids:
            cursor.execute("DELETE FROM premium_role_users WHERE expiration_time < ? AND role_tier = ?",
                           (current_time, role_tier))
            return expired_premium_role_users_ids
