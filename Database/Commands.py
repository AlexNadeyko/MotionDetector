import sqlite3
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash


def insert_into_log(log):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO log (date_time,is_known,face_image)
                            VALUES(?,?,?)''', log)
    return cursor.lastrowid


def insert_into_user(user):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO user (login,hashed_password)
                            VALUES(?,?)''', user)
    return cursor.lastrowid

def select_from_log():
    conn = connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM log')
        rows = cursor.fetchall()
    return rows


def select_from_user():
    conn = connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user')
        rows = cursor.fetchall()
    return rows


def find_db_path():
    db_regex = '.*db$'

    for file_name in os.listdir(r'Database'):
        db_path = re.findall(db_regex, file_name)
        if len(db_path) > 0:
            return db_path[0]

    return None

def connect():
    conn = None
    try:
        db_path = find_db_path()

        conn = sqlite3.connect(f'Database/{db_path}')
        return conn

    except Exception as e:
        print(f'Something went wrong: {e}')


def check_if_user_exist(login, password):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        sql_select_query = """SELECT * FROM user WHERE login = ?"""
        hashed_password = generate_password_hash(password)
        cursor.execute(sql_select_query, (login,))
        user = cursor.fetchall()

        if check_password_hash(user[0][1], password):
            print("True")
            return True
        else:
            print("False")
            return False


