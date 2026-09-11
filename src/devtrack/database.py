import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]


def get_connection():
    return psycopg.connect(DATABASE_URL)


def create_tables():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """
        )
        connection.commit()


def select_tasks():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT id, title, status FROM tasks")
        rows = cursor.fetchall()

        return rows
