import sqlite3
from sqlite3 import Error


def create_connection(db_file: str) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        print(f"Соединение с {db_file} успешно установлено.")
    except Error as e:
        print(e)

    return conn


def create_table(conn: sqlite3.Connection, create_table_sql: str) -> None:
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Таблица успешно создана.")
    except Error as e:
        print(e)


def insert_table(conn: sqlite3.Connection, sql: str, param: tuple[str]) -> None:
    try:
        cur = conn.cursor()
        cur.execute(sql, param)
        conn.commit()
        print("Вставка успешно произведена")
    except Error as e:
        print(e)


def select_all_prediction(conn: sqlite3.Connection) -> list[str]:
    cur = conn.cursor()
    cur.execute(f"SELECT text FROM prediction")

    rows = cur.fetchall()
    result = []

    for row in rows:
        result.append(row[0])

    return result

def select_all_table(conn: sqlite3.Connection, table_name: str) -> list[tuple[str]]:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")

    rows = cur.fetchall()

    return rows


def close_connection(conn: sqlite3.Connection) -> None:
    if conn:
        conn.close()
        print("Соединение закрыто.")
