import sqlite3

conn = sqlite3.connect("cynthiabot.db")


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


conn.row_factory = dict_factory

cur = conn.cursor()


def add_subscription(name: str, num1: int = None, num2: int = None, other: str = None):
    sql = "INSERT INTO subscriptions VALUES (?, ?, ?, ?)"
    parameters = (name, num1, num2, other)

    cur.execute(sql, parameters)


def delete_subscription(name: str, num1: int):
    sql = "DELETE FROM subscriptions WHERE name=? AND num1=?"
    parameters = (name, num1)

    cur.execute(sql, parameters)


def get_all_subscriptions():
    sql = "SELECT * FROM subscriptions"

    res = cur.execute(sql)

    return res.fetchall()


def get_subscription(name: str, num1: int = None, num2: int = None, other: str = None):
    sql = "SELECT * FROM subscriptions WHERE name=?"
    parameters = (p for p in [name, num1, num2, other] if p is not None)

    if num1:
        sql += " AND num1=?"
    if num2:
        sql += " AND num2=?"
    if other:
        sql += " AND other=?"

    res = cur.execute(sql, parameters)

    return res.fetchall()
