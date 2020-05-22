import sqlite3
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash


def insert_into_user(user):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO user (login,hashed_password)
                            VALUES(?,?)''', user)
    return cursor.lastrowid

def insert_into_user_to_add(user):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO user_to_add (login, hashed_password, date_time)
                            VALUES(?,?,?)''', user)
    return cursor.lastrowid

def select_from_log():
    conn = connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM log ORDER BY date desc, time desc')
        rows = cursor.fetchall()
    return rows


def select_from_user():
    conn = connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user')
        rows = cursor.fetchall()
    return rows


def select_image_from_log(id_record):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        sql_select_query = ("""SELECT * FROM log WHERE id_record = ?""")
        cursor.execute(sql_select_query, (id_record,))
        result = cursor.fetchall()

    image = result[0][4]
    return image


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
        if user:
            if check_password_hash(user[0][1], password):
                return True
            else:
                return False
        else:
            return False


def check_if_user_exist_user_table(login):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        sql_select_query = """SELECT * FROM user WHERE login = ?"""
        cursor.execute(sql_select_query, (login,))
        user = cursor.fetchall()
        if user:
            return True
        else:
            return False


def check_if_user_exist_user_to_add_table(login):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        sql_select_query = """SELECT * FROM user_to_add WHERE login = ?"""
        cursor.execute(sql_select_query, (login,))
        user = cursor.fetchall()
        if user:
            return True
        else:
            return False


def insert_into_log(log_faces_recognition):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        sql_insert_query = '''INSERT INTO log (date, time, person, face_image)
                            VALUES(?,?,?,?)'''
        for log_entry in log_faces_recognition:
            cursor.execute(sql_insert_query, log_entry)

    return cursor.lastrowid








