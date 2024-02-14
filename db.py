from psycopg_pool import ConnectionPool
from os import getenv
from dotenv import load_dotenv

load_dotenv()
pool = ConnectionPool(conninfo=getenv("DATABASE_URL"), timeout = 10, max_lifetime=600)

class DataBase:
    def is_user(user_id: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
                result = cursor.fetchone()
                return result

    def insert_user(user_id: int, username: str):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users(user_id, username, chatgpt, dall_e, stable_diffusion) VALUES (%s, %s, %s, %s, %s)", (user_id,username,3000,3,3))
                conn.commit()

    def get_chatgpt(user_id: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT chatgpt FROM users WHERE user_id = '{user_id}'")
                result = int(cursor.fetchone()[0])
                return result

    def set_chatgpt(user_id: int, result: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"UPDATE users SET chatgpt = {result} WHERE user_id = '{user_id}'")
                conn.commit()

    def get_dalle(user_id: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT dall_e FROM users WHERE user_id = '{user_id}'")
                result = int(cursor.fetchone()[0])
                return result

    def set_dalle(user_id: int, result: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"UPDATE users SET dall_e = {result} WHERE user_id = '{user_id}'")
                conn.commit()

    def get_stable(user_id: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT stable_diffusion FROM users WHERE user_id = '{user_id}'")
                result = int(cursor.fetchone()[0])
                return result

    def set_stable(user_id: int, result: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"UPDATE users SET stable_diffusion = {result} WHERE user_id = '{user_id}'")
                conn.commit()

    def get_userinfo(user_id: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
                result = cursor.fetchone()
                return result

    def new_order(invoice_id: int, user_id: int, product: str):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO orders(invoice_id, user_id, product) VALUES (%s, %s, %s)", (invoice_id, user_id, product))
                conn.commit()

    def get_orderdata(invoice_id: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT user_id, product FROM orders WHERE invoice_id = {invoice_id}")
                result = cursor.fetchone()
                return result

    def update_chatgpt(user_id: int, invoice_id: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"UPDATE users SET chatgpt = chatgpt + 100000 WHERE user_id = '{user_id}'")
                cursor.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
                conn.commit()

    def update_dalle(user_id: int, invoice_id: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"UPDATE users SET dall_e = dall_e + 100 WHERE user_id = '{user_id}'")
                cursor.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
                conn.commit()

    def update_stable(user_id: int, invoice_id: int):
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"UPDATE users SET stable_diffusion = stable_diffusion + 100 WHERE user_id = '{user_id}'")
                cursor.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
                conn.commit()
