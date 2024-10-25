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
        cursor.execute("""CREATE TABLE IF NOT EXISTS premium_role_lite_owners (
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
        cursor.execute("SELECT user_discord_name, balance FROM user_balances WHERE balance > 0 ORDER BY balance DESC")
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
        cursor.execute("SELECT balance FROM user_balances WHERE user_discord_id = ?", (user.id,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO user_balances (user_discord_id, user_discord_name) VALUES (?, ?)",
                           (user.id, user.name))
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


@catch_sql_exceptions
def add_premium_role_owner(user, expiration_time, lite=False):
    premium_table = "premium_role_owners" if not lite else "premium_role_lite_owners"
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {premium_table} WHERE user_discord_id = ?",
                       (user.id,))
        user_exists = cursor.fetchone()[0]
        if user_exists:
            cursor.execute(f"UPDATE {premium_table} SET user_discord_name = ?, expiration_time = ? WHERE user_discord_id = ?",
                           (user.name, expiration_time, user.id))
        else:
            cursor.execute(f"INSERT INTO {premium_table} (user_discord_id, user_discord_name, expiration_time) VALUES (?, ?, ?)",
                           (user.id, user.name, expiration_time))


@catch_sql_exceptions
def get_all_premium_role_owners(lite=False):
    premium_table = "premium_role_owners" if not lite else "premium_role_lite_owners"
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute(f"SELECT user_discord_name, expiration_time FROM {premium_table}")
        return cursor.fetchall()


@catch_sql_exceptions
def remove_expired_premium_role_owners(current_time, lite=False):
    premium_table = "premium_role_owners" if not lite else "premium_role_lite_owners"
    with sqlite3.connect(config.DATABASE_PATH) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute(f"SELECT user_discord_id FROM {premium_table} WHERE expiration_time < ?",
                       (current_time,))
        expired_premium_role_owners_ids = cursor.fetchall()
        if expired_premium_role_owners_ids:
            cursor.execute(f"DELETE FROM {premium_table} WHERE expiration_time < ?",
                           (current_time, ))
            return expired_premium_role_owners_ids
