from psycopg_pool import AsyncConnectionPool
from os import getenv
from dotenv import load_dotenv
from typing import List, Tuple, Dict

load_dotenv()
pool = AsyncConnectionPool(conninfo=getenv("DATABASE_URL"), timeout = 10, max_lifetime=600, check=AsyncConnectionPool.check_connection, open = False)

class DataBase:
    async def open_pool():
        await pool.open()
        await pool.wait()
    async def is_user(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id, ))
                result = await cursor.fetchone()
                return result
    async def insert_user(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("INSERT INTO users(user_id, chatgpt, dall_e, stable_diffusion) VALUES (%s, %s, %s, %s)", (user_id,3000,3,3))
                await conn.commit()
    async def get_chatgpt(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT chatgpt FROM users WHERE user_id = %s", (user_id, ))
                result = int((await cursor.fetchone())[0])
                return result
    async def set_chatgpt(user_id: int, result: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE users SET chatgpt = %s WHERE user_id = %s", (result, user_id))
                await conn.commit()
    async def get_dalle(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT dall_e FROM users WHERE user_id = %s", (user_id, ))
                result = int((await cursor.fetchone())[0])
                return result
    async def set_dalle(user_id: int, result: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE users SET dall_e = %s WHERE user_id = %s", (result, user_id))
                await conn.commit()
    async def get_stable(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT stable_diffusion FROM users WHERE user_id = %s", (user_id, ))
                result = int((await cursor.fetchone())[0])
                return result
    async def set_stable(user_id: int, result: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE users SET stable_diffusion = %s WHERE user_id = %s", (result, user_id))
                await conn.commit()
    async def get_userinfo(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT chatgpt, dall_e, stable_diffusion FROM users WHERE user_id = %s", (user_id, ))
                result = await cursor.fetchone()
                return result
    async def new_order(invoice_id: int, user_id: int, product: str):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("INSERT INTO orders(invoice_id, user_id, product) VALUES (%s, %s, %s)", (invoice_id, user_id, product))
                await conn.commit()
    async def get_orderdata(invoice_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT user_id, product FROM orders WHERE invoice_id = %s", (invoice_id, ))
                result = await cursor.fetchone()
                return result
    async def update_chatgpt(user_id: int, invoice_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE users SET chatgpt = chatgpt + 100000 WHERE user_id = %s", (user_id, ))
                await cursor.execute("DELETE FROM orders WHERE invoice_id = %s", (invoice_id, ))
                await conn.commit()
    async def update_dalle(user_id: int, invoice_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE users SET dall_e = dall_e + 50 WHERE user_id = %s", (user_id, ))
                await cursor.execute("DELETE FROM orders WHERE invoice_id = %s", (invoice_id, ))
                await conn.commit()
    async def update_stable(user_id: int, invoice_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE users SET stable_diffusion = stable_diffusion + 50 WHERE user_id = %s", (user_id, ))
                await cursor.execute("DELETE FROM orders WHERE invoice_id = %s", (invoice_id, ))
                await conn.commit()
    async def save_message(user_id: int, role: str, message: str, tokens: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                conn.commit()
                await cursor.execute("INSERT INTO messages(user_id, role, content, tokens) VALUES (%s, %s, %s, %s)", (user_id, role, message, tokens))
                await conn.commit()
    async def delete_messages(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM messages WHERE user_id = %s", (user_id,))
                await conn.commit()
    async def get_messages(user_id: int) -> Tuple[List[Dict[str, str]], int]:
        async with pool.connection() as conn:
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
