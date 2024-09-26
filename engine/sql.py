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
        cursor.execute("""CREATE TABLE IF NOT EXISTS premium_role_owners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_discord_id INTEGER NOT NULL,
            user_discord_name TEXT NOT NULL,
            expiration_time INTEGER NOT NULL
            )""")
        cursor.execute("""INSERT INTO bank_balance (balance)
            SELECT 0
            WHERE NOT EXISTS (SELECT 1 FROM bank_balance
            )""")


@catch_sql_exceptions
def create_user_balance(user_discord_id, user_discord_name):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("INSERT INTO user_balances (user_discord_id, user_discord_name) VALUES (?, ?)",
                       (user_discord_id, user_discord_name))


@catch_sql_exceptions
def get_user_balance(user_discord_id):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT balance FROM user_balances WHERE user_discord_id = ?",
                       (user_discord_id,))
        row = cursor.fetchone()
        return row[0] if row else None


@catch_sql_exceptions
def get_all_users_balances():
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT user_discord_name, balance FROM user_balances WHERE balance > 0 ORDER BY balance DESC")
        return cursor.fetchall()


@catch_sql_exceptions
def get_last_catching_time(user_discord_id):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT last_catching_time FROM user_balances WHERE user_discord_id = ?",
                       (user_discord_id,))
        return cursor.fetchone()[0]


@catch_sql_exceptions
def set_user_balance(user_discord_id, amount):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("UPDATE user_balances SET balance = balance + ? WHERE user_discord_id = ?",
                       (amount, user_discord_id,))


@catch_sql_exceptions
def set_last_catching_time(user_discord_id, current_time):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("UPDATE user_balances SET last_catching_time = ? WHERE user_discord_id = ?",
                       (current_time, user_discord_id,))


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


@catch_sql_exceptions
def add_premium_role_owner(user_discord_id, user_discord_name, expiration_time):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT COUNT(*) FROM premium_role_owners WHERE user_discord_id = ?",
                       (user_discord_id,))
        user_exists = cursor.fetchone()[0]
        if user_exists:
            cursor.execute("""
                        UPDATE premium_role_owners SET user_discord_name = ?, expiration_time = ?WHERE user_discord_id = ?""",
                           (user_discord_name, expiration_time, user_discord_id))
        else:
            cursor.execute("INSERT INTO premium_role_owners (user_discord_id, user_discord_name, expiration_time) VALUES (?, ?, ?)",
                           (user_discord_id, user_discord_name, expiration_time))


@catch_sql_exceptions
def get_all_premium_role_owners():
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT user_discord_name, expiration_time FROM premium_role_owners")
        return cursor.fetchall()


@catch_sql_exceptions
def remove_expired_premium_role_owners(current_time):
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute("SELECT user_discord_id FROM premium_role_owners WHERE expiration_time < ?",
                       (current_time,))
        expired_premium_role_owners_ids = cursor.fetchall()
        if expired_premium_role_owners_ids:
            cursor.execute("DELETE FROM premium_role_owners WHERE expiration_time < ?",
                           (current_time, ))
            return expired_premium_role_owners_ids
