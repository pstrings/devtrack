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


def insert_task(title: str, status: str):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO tasks (title, status) VALUES (%s, %s) RETURNING id, title, status", (title, status))

        row = cursor.fetchone()

        connection.commit()

        return row
