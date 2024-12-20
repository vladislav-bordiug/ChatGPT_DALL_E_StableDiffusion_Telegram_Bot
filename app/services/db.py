from psycopg_pool import AsyncConnectionPool
from typing import List, Tuple, Dict
import logging

class DatabaseError(Exception):
    def __init__(self, msg: str = "Error"):
        self.msg=msg
    def output(self):
        logging.error("Database error:", self.msg)

class DataBase:
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool
    async def create_tables(self):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY, chatgpt INT, dall_e INT, stable_diffusion INT)")
                    await cursor.execute("CREATE TABLE IF NOT EXISTS orders (invoice_id INT PRIMARY KEY, user_id BIGINT, product TEXT, FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE)")
                    await cursor.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, user_id BIGINT, role TEXT, content TEXT, tokens INT, FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE)")
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def is_user(self, user_id: int) -> Tuple[int]:
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id, ))
                    result = await cursor.fetchone()
                    return result
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def insert_user(self, user_id: int):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO users(user_id, chatgpt, dall_e, stable_diffusion) VALUES (%s, %s, %s, %s)", (user_id,3000,3,3))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def get_chatgpt(self, user_id: int) -> int:
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT chatgpt FROM users WHERE user_id = %s", (user_id, ))
                    result = (await cursor.fetchone())[0]
                    return result
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def set_chatgpt(self, user_id: int, result: int):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("UPDATE users SET chatgpt = %s WHERE user_id = %s", (result, user_id))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def get_dalle(self, user_id: int) -> int:
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT dall_e FROM users WHERE user_id = %s", (user_id, ))
                    result = (await cursor.fetchone())[0]
                    return result
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def set_dalle(self, user_id: int, result: int):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("UPDATE users SET dall_e = %s WHERE user_id = %s", (result, user_id))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def get_stable(self, user_id: int) -> int:
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT stable_diffusion FROM users WHERE user_id = %s", (user_id, ))
                    result = (await cursor.fetchone())[0]
                    return result
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def set_stable(self, user_id: int, result: int):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("UPDATE users SET stable_diffusion = %s WHERE user_id = %s", (result, user_id))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def get_userinfo(self, user_id: int) -> Tuple[int, int, int]:
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT chatgpt, dall_e, stable_diffusion FROM users WHERE user_id = %s", (user_id, ))
                    result = await cursor.fetchone()
                    return result
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def new_order(self, invoice_id: int, user_id: int, product: str):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO orders(invoice_id, user_id, product) VALUES (%s, %s, %s)", (invoice_id, user_id, product))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def get_orderdata(self, invoice_id: int) -> Tuple[int, str]:
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT user_id, product FROM orders WHERE invoice_id = %s", (invoice_id, ))
                    result = await cursor.fetchone()
                    return result
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def update_chatgpt(self, user_id: int, invoice_id: int):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("UPDATE users SET chatgpt = chatgpt + 100000 WHERE user_id = %s", (user_id, ))
                    await cursor.execute("DELETE FROM orders WHERE invoice_id = %s", (invoice_id, ))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def update_dalle(self, user_id: int, invoice_id: int):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("UPDATE users SET dall_e = dall_e + 50 WHERE user_id = %s", (user_id, ))
                    await cursor.execute("DELETE FROM orders WHERE invoice_id = %s", (invoice_id, ))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def update_stable(self, user_id: int, invoice_id: int):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("UPDATE users SET stable_diffusion = stable_diffusion + 50 WHERE user_id = %s", (user_id, ))
                    await cursor.execute("DELETE FROM orders WHERE invoice_id = %s", (invoice_id, ))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def save_message(self, user_id: int, role: str, message: str, tokens: int):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO messages(user_id, role, content, tokens) VALUES (%s, %s, %s, %s)", (user_id, role, message, tokens))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def delete_messages(self, user_id: int):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("DELETE FROM messages WHERE user_id = %s", (user_id,))
                    await conn.commit()
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err
    async def get_messages(self, user_id: int) -> Tuple[List[Dict[str, str]], int]:
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("""
                    WITH cte AS (
                        SELECT 
                            id, 
                            role, 
                            content, 
                            tokens,
                            SUM(tokens) OVER (ORDER BY id DESC) AS tokens_total
                        FROM messages
                        WHERE user_id = %s
                    )
                    SELECT role, content, tokens_total
                    FROM cte
                    WHERE tokens_total <= 128000
                    ORDER BY id ASC;""", (user_id,))
                    result = await cursor.fetchall()
                    if not result:
                        return [], 0
                    return [{"role": role, "content": content}  for role, content, _ in result], result[0][2]
        except Exception as e:
            err = DatabaseError(str(e))
            err.output()
            raise err