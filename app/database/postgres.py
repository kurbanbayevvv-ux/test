import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
conn = psycopg2.connect(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASS'),
        host = os.getenv('DB_HOST'),
        port = os.getenv('DB_PORT')
    )

cur = conn.cursor()


def Register(chat_id, first_name):
    sql = "SELECT * FROM users WHERE chat_id = %s"
    cur.execute(sql, (chat_id,))
    result = cur.fetchone()
    if not result:
        sql = "INSERT INTO users (chat_id, phone_number) VALUES (%s, %s)"
        cur.execute(sql, (chat_id, first_name))
        conn.commit()

def addUserInfo(chat_id, full_name, phone_number):
    sql = """
    INSERT INTO users (chat_id, phone_number, full_name)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (chat_id, phone_number, full_name))
    conn.commit()

def user(chat_id):
    sql = "SELECT 1 FROM users WHERE chat_id = %s"
    cur.execute(sql, (chat_id,))
    return cur.fetchone()