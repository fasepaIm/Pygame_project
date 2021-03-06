# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеки
import sqlite3


def add_record(name, score, mode):
    con = sqlite3.connect("assets/records_db/score.db")
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    if 'NORMAL' in mode:
        index = cur.execute("""SELECT MIN(score), id FROM records_normal""").fetchall()[0]
        result = cur.execute(f"""UPDATE records_normal
                                 SET name = '{name}', score = '{score}'
                                 WHERE {score} > {index[0]} AND id = {index[1]}""")
        con.commit()
    elif 'NIGHT' in mode:
        index = cur.execute("""SELECT MIN(score), id FROM records_night""").fetchall()[0]
        result = cur.execute(f"""UPDATE records_night
                                 SET name = '{name}', score = '{score}'
                                 WHERE {score} > {index[0]} AND id = {index[1]}""")
        con.commit()
    elif 'HARD' in mode:
        index = cur.execute("""SELECT MIN(score), id FROM records_hard""").fetchall()[0]
        result = cur.execute(f"""UPDATE records_hard
                                 SET name = '{name}', score = '{score}'
                                 WHERE {score} > {index[0]} AND id = {index[1]}""")
        con.commit()
    con.close()


def score_table(mode):
    con = sqlite3.connect("assets/records_db/score.db")
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    if 'NORMAL' in mode:
        result = cur.execute("""SELECT name, score FROM records_normal""").fetchall()
    elif 'NIGHT' in mode:
        result = cur.execute("""SELECT name, score FROM records_night""").fetchall()
    elif 'HARD' in mode:
        result = cur.execute("""SELECT name, score FROM records_hard""").fetchall()
    values = sorted(result, key=lambda x: x[1], reverse=True)
    con.close()
    return values
