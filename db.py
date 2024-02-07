import psycopg2
import os
from dotenv import load_dotenv

class DataBase:
    def __init__(self):
        load_dotenv()
        self.db_connection = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
        self.db_object = self.db_connection.cursor()

    def is_user(self,user_id: int):
        self.db_object.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        result = self.db_object.fetchone()
        return result

    def insert_user(self,user_id: int, username: str):
        self.db_object.execute("INSERT INTO users(user_id, username, chatgpt, dall_e, stable_diffusion) VALUES (%s, %s, %s, %s, %s)",(user_id, username, 3000, 3, 3))
        self.db_connection.commit()
        return

    def get_chatgpt(self,user_id: int):
        self.db_object.execute(f"SELECT chatgpt FROM users WHERE user_id = '{user_id}'")
        result = int(self.db_object.fetchone()[0])
        return result

    def set_chatgpt(self,user_id: int, result: int):
        self.db_object.execute(f"UPDATE users SET chatgpt = {result} WHERE user_id = '{user_id}'")
        self.db_connection.commit()
        return result

    def get_dalle(self,user_id: int):
        self.db_object.execute(f"SELECT dall_e FROM users WHERE user_id = '{user_id}'")
        result = int(self.db_object.fetchone()[0])
        return result

    def set_dalle(self,user_id: int, result: int):
        self.db_object.execute(f"UPDATE users SET dall_e = {result} WHERE user_id = '{user_id}'")
        self.db_connection.commit()
        return result

    def get_stable(self,user_id: int):
        self.db_object.execute(f"SELECT stable_diffusion FROM users WHERE user_id = '{user_id}'")
        result = int(self.db_object.fetchone()[0])
        return result

    def set_stable(self,user_id: int, result: int):
        self.db_object.execute(f"UPDATE users SET stable_diffusion = {result} WHERE user_id = '{user_id}'")
        self.db_connection.commit()
        return result

    def get_userinfo(self,user_id: int):
        self.db_object.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
        result = self.db_object.fetchone()
        return result

    def new_order(self,invoice_id: int, user_id: int, product: str):
        self.db_object.execute("INSERT INTO orders(invoice_id, user_id, product) VALUES (%s, %s, %s)", (invoice_id, user_id, product))
        self.db_connection.commit()
        return

    def get_orderdata(self,invoice_id: int):
        self.db_object.execute(f"SELECT user_id, product FROM orders WHERE invoice_id = {invoice_id}")
        result = self.db_object.fetchone()
        return result

    def update_chatgpt(self,user_id: int, invoice_id: int):
        self.db_object.execute(f"UPDATE users SET chatgpt = chatgpt + 100000 WHERE user_id = '{user_id}'")
        self.db_object.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
        self.db_connection.commit()
        return

    def update_dalle(self,user_id: int, invoice_id: int):
        self.db_object.execute(f"UPDATE users SET dall_e = dall_e + 100 WHERE user_id = '{user_id}'")
        self.db_object.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
        self.db_connection.commit()
        return

    def update_stable(self,user_id: int, invoice_id: int):
        self.db_object.execute(f"UPDATE users SET stable_diffusion = stable_diffusion + 100 WHERE user_id = '{user_id}'")
        self.db_object.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
        self.db_connection.commit()
        return