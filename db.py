import psycopg2
from os import getenv
from dotenv import load_dotenv
from threading import Lock

load_dotenv()
db_connection = psycopg2.connect(getenv("DATABASE_URL"), sslmode="require")
db_object = db_connection.cursor()
lock = Lock()

class DataBase:

    def is_user(user_id: int):
        lock.acquire()
        db_object.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        result = db_object.fetchone()
        lock.release()
        return result

    def insert_user(user_id: int, username: str):
        lock.acquire()
        db_object.execute("INSERT INTO users(user_id, username, chatgpt, dall_e, stable_diffusion) VALUES (%s, %s, %s, %s, %s)",(user_id, username, 3000, 3, 3))
        db_connection.commit()
        lock.release()

    def get_chatgpt(user_id: int):
        lock.acquire()
        db_object.execute(f"SELECT chatgpt FROM users WHERE user_id = '{user_id}'")
        result = int(db_object.fetchone()[0])
        lock.release()
        return result

    def set_chatgpt(user_id: int, result: int):
        lock.acquire()
        db_object.execute(f"UPDATE users SET chatgpt = {result} WHERE user_id = '{user_id}'")
        db_connection.commit()
        lock.release()
        return result

    def get_dalle(user_id: int):
        lock.acquire()
        db_object.execute(f"SELECT dall_e FROM users WHERE user_id = '{user_id}'")
        result = int(db_object.fetchone()[0])
        lock.release()
        return result

    def set_dalle(user_id: int, result: int):
        lock.acquire()
        db_object.execute(f"UPDATE users SET dall_e = {result} WHERE user_id = '{user_id}'")
        db_connection.commit()
        lock.release()
        return result

    def get_stable(user_id: int):
        lock.acquire()
        db_object.execute(f"SELECT stable_diffusion FROM users WHERE user_id = '{user_id}'")
        result = int(db_object.fetchone()[0])
        lock.release()
        return result

    def set_stable(user_id: int, result: int):
        lock.acquire()
        db_object.execute(f"UPDATE users SET stable_diffusion = {result} WHERE user_id = '{user_id}'")
        db_connection.commit()
        lock.release()
        return result

    def get_userinfo(user_id: int):
        lock.acquire()
        db_object.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
        result = db_object.fetchone()
        lock.release()
        return result

    def new_order(invoice_id: int, user_id: int, product: str):
        lock.acquire()
        db_object.execute("INSERT INTO orders(invoice_id, user_id, product) VALUES (%s, %s, %s)", (invoice_id, user_id, product))
        db_connection.commit()
        lock.release()

    def get_orderdata(invoice_id: int):
        lock.acquire()
        db_object.execute(f"SELECT user_id, product FROM orders WHERE invoice_id = {invoice_id}")
        result = db_object.fetchone()
        lock.release()
        return result

    def update_chatgpt(user_id: int, invoice_id: int):
        lock.acquire()
        db_object.execute(f"UPDATE users SET chatgpt = chatgpt + 100000 WHERE user_id = '{user_id}'")
        db_object.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
        db_connection.commit()
        lock.release()

    def update_dalle(user_id: int, invoice_id: int):
        lock.acquire()
        db_object.execute(f"UPDATE users SET dall_e = dall_e + 100 WHERE user_id = '{user_id}'")
        db_object.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
        db_connection.commit()
        lock.release()

    def update_stable(user_id: int, invoice_id: int):
        lock.acquire()
        db_object.execute(f"UPDATE users SET stable_diffusion = stable_diffusion + 100 WHERE user_id = '{user_id}'")
        db_object.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
        db_connection.commit()
        lock.release()