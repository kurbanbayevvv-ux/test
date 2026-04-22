import psycopg2
import os
from dotenv import load_dotenv

from utils.generate_card_number import generateCardNumber

from datetime import date
from dateutil.relativedelta import relativedelta

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        chat_id BIGINT UNIQUE NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        name VARCHAR(100),
        page VARCHAR(255) DEFAULT 'home',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        id SERIAL PRIMARY KEY,
        user_chat_id BIGINT REFERENCES users(chat_id),
        balance INT DEFAULT 0,
        number BIGINT NOT NULL UNIQUE,
        valid DATE NOT NULL,
        card_type VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

def Register(chat_id, first_name):
    sql = "SELECT * FROM users WHERE chat_id = %s"
    cur.execute(sql, (chat_id,))
    result = cur.fetchone()
    if not result:
        sql = "INSERT INTO users (chat_id, first_name) VALUES (%s, %s)"
        cur.execute(sql, (chat_id, first_name))
        conn.commit()

def get_all_balance(chat_id):
    sql = "SELECT * FROM cards WHERE user_chat_id = %s"
    cur.execute(sql, (chat_id,))
    result = cur.fetchall()
    if result:
        sql = "SELECT SUM(balance) FROM cards WHERE user_chat_id = %s"
        cur.execute(sql, (chat_id,))
        return cur.fetchone()[0]
    return 'Karta mavjud emas!'

def get_all_cards(chat_id):
    sql = "SELECT number FROM cards WHERE user_chat_id = %s"
    cur.execute(sql, (chat_id,))
    return cur.fetchall()

def create_card(chat_id, type):
    card_number = generateCardNumber()
    valid = date.today() + relativedelta(years=3)
    valid = valid.strftime('%Y-%m-%d')
    sql = ("INSERT INTO cards (user_chat_id, number, valid, card_type)"
           "VALUES (%s, %s, %s, %s)")
    cur.execute(sql, (chat_id, card_number, valid, type))
    conn.commit()

def get_card(card_number):
    sql = "SELECT number, balance, card_type, valid FROM cards WHERE number = %s"
    cur.execute(sql, (card_number,))
    return cur.fetchone()

def getPage(chat_id):
    sql = "SELECT page FROM users WHERE chat_id = %s"
    cur.execute(sql, (chat_id,))
    return cur.fetchone()[0]

def setPage(chat_id, page):
    sql = "UPDATE users SET page = %s WHERE chat_id = %s"
    cur.execute(sql, (page, chat_id))
    conn.commit()

def get_card_owner(card_number):
    sql = "SELECT user_chat_id FROM cards WHERE number = %s"
    cur.execute(sql, (card_number,))
    result = cur.fetchone()
    if result:
        sql = "SELECT first_name FROM users WHERE chat_id = %s"
        cur.execute(sql, (result[0],))
        return cur.fetchone()[0]

def card_to_card(card1, card2, summa):
    card1_balance = get_card(card1)[1]
    if int(card1_balance) >= int(summa):
        sql = "UPDATE cards SET balance = balance - %s WHERE number = %s"
        cur.execute(sql, (summa, card1))
        sql = "UPDATE cards SET balance = balance + %s WHERE number = %s"
        cur.execute(sql, (summa, card2))
        conn.commit()