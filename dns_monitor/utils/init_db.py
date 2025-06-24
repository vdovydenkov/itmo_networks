import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

dsn = os.getenv("DB_DSN")

# SQL-команды создания таблиц
CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS http_logs (
        id SERIAL PRIMARY KEY,
        ip TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        path TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS dns_logs (
        id SERIAL PRIMARY KEY,
        resolver_ip TEXT NOT NULL,
        domain TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS as_info (
        ip TEXT PRIMARY KEY,
        asn TEXT,
        asn_desc TEXT
    )
    """
]

def init_db():
    try:
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cursor:
                for command in CREATE_TABLES:
                    cursor.execute(command)
            conn.commit()
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")

if __name__ == "__main__":
    init_db()
