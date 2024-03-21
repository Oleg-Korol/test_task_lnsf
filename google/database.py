import logging
import sqlite3
from collections import namedtuple
from logs.logging_settings import setup_logging

setup_logging()


def create_db(name_db: str) -> None:
    """
    Создаем подключение к базе данных (если базы данных нет, она будет создана)
    """
    try:
        with sqlite3.connect(name_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                first_name TEXT,
                                last_name TEXT,
                                login TEXT UNIQUE,
                                password TEXT,
                                email TEXT
                            )''')
            conn.commit()
            logging.info('База данных успешно создана')

    except sqlite3.Error as err:
        logging.warning(f'Произошла ошибка при создании базы данных: {err}')



def db_add_account(account: namedtuple) -> None:
    """
    Добавляем данные аккаунта в базу данных
    """
    try:
        with sqlite3.connect('user_db') as conn:

            cursor = conn.cursor()
            # Проверяем, существует ли уже аккаунт с таким логином
            cursor.execute('SELECT id FROM users WHERE login = ?', (account.login,))
            existing_account = cursor.fetchone()
            if existing_account:
                # Если аккаунт существует, обновляем его данные
                sql_query = '''
                            UPDATE users
                            SET first_name = ?, last_name = ?, password = ?, email = ?
                            WHERE login = ?
                            '''
                data_to_update = (account.first_name, account.last_name, account.password, account.email, account.login)
                cursor.execute(sql_query, data_to_update)
            else:
                # Если аккаунт не существует, добавляем новый
                sql_query = '''
                            INSERT INTO users (first_name, last_name, login, password, email)
                            VALUES (?, ?, ?, ?, ?)
                            '''
                data_to_insert = (account.first_name, account.last_name, account.login, account.password, account.email)
                cursor.execute(sql_query, data_to_insert)
            conn.commit()
            logging.info(f'Аккаунт {account.login} успешно добавлен или обновлен в базе данных')

    except sqlite3.Error as err:
        logging.warning(f'Произошла ошибка при добавлении аккаунта в базу данных: {err}')
