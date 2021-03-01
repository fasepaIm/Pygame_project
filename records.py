# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеки
import sqlite3


def add_record(name, score, mode):
    con = sqlite3.connect("assets/records_db/score.db")
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    if 'NORMAL' in mode:
        result = cur.execute(f"""UPDATE records_normal
                                 SET name = '{name}', score = '{score}'
                                 WHERE {score} > (
                                 SELECT MIN(score) FROM records_normal) AND name =(
                                 SELECT name FROM records_normal WHERE score=(
                                 SELECT MIN(score) FROM records_normal))""")
        con.commit()
    elif 'NIGHT' in mode:
        result = cur.execute(f"""UPDATE records_night
                                 SET name = '{name}', score = '{score}'
                                 WHERE {score} > (
                                 SELECT MIN(score) FROM records_night) AND name =(
                                 SELECT name FROM records_night WHERE score=(
                                 SELECT MIN(score) FROM records_night))""")
        con.commit()
    elif 'HARD' in mode:
        result = cur.execute(f"""UPDATE records_hard
                                 SET name = '{name}', score = '{score}'
                                 WHERE {score} > (
                                 SELECT MIN(score) FROM records_hard) AND name =(
                                 SELECT name FROM records_hard WHERE score=(
                                 SELECT MIN(score) FROM records_hard))""")
        con.commit()
    con.close()

def score_table(mode):
    con = sqlite3.connect("assets/records_db/score.db")
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    if 'NORMAL' in mode:
        result = cur.execute("""SELECT * FROM records_normal""").fetchall()
    elif 'NIGHT' in mode:
        result = cur.execute("""SELECT * FROM records_night""").fetchall()
    elif 'HARD' in mode:
        result = cur.execute("""SELECT * FROM records_hard""").fetchall()
    values = sorted(result, key=lambda x: x[1], reverse=True)
    con.close()
    return values
