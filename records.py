# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеки
import sqlite3


# Подключение к БД
def add_record(name, score):
    con = sqlite3.connect("assets/records_db/score.db")
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    result = cur.execute(f"""INSERT INTO records(name, score) VALUES('{name}', {score})""")
    con.commit()
    con.close()


def score_table():
    con = sqlite3.connect("assets/records_db/score.db")
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    result = cur.execute("""SELECT * FROM records""").fetchall()
    result = sorted(result, key=lambda x: x[1], reverse=True)
    con.close()
    return result
