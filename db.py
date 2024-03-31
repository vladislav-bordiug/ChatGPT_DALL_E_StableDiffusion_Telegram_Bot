from psycopg_pool import AsyncConnectionPool
from os import getenv
from dotenv import load_dotenv

load_dotenv()
pool = AsyncConnectionPool(conninfo=getenv("DATABASE_URL"), timeout = 10, max_lifetime=600, check=AsyncConnectionPool.check_connection, open = False)

class DataBase:
    async def open_pool():
        await pool.open()
        await pool.wait()
    async def is_user(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
                result = await cursor.fetchone()
                return result
    async def insert_user(user_id: int, username: str):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("INSERT INTO users(user_id, username, chatgpt, dall_e, stable_diffusion) VALUES (%s, %s, %s, %s, %s)", (user_id,username,3000,3,3))
                await conn.commit()
    async def get_chatgpt(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT chatgpt FROM users WHERE user_id = '{user_id}'")
                result = int((await cursor.fetchone())[0])
                return result
    async def set_chatgpt(user_id: int, result: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET chatgpt = {result} WHERE user_id = '{user_id}'")
                await conn.commit()
    async def get_dalle(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT dall_e FROM users WHERE user_id = '{user_id}'")
                result = int((await cursor.fetchone())[0])
                return result
    async def set_dalle(user_id: int, result: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET dall_e = {result} WHERE user_id = '{user_id}'")
                await conn.commit()
    async def get_stable(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT stable_diffusion FROM users WHERE user_id = '{user_id}'")
                result = int((await cursor.fetchone())[0])
                return result
    async def set_stable(user_id: int, result: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET stable_diffusion = {result} WHERE user_id = '{user_id}'")
                await conn.commit()
    async def get_userinfo(user_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
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
                await cursor.execute(f"SELECT user_id, product FROM orders WHERE invoice_id = {invoice_id}")
                result = await cursor.fetchone()
                return result
    async def update_chatgpt(user_id: int, invoice_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET chatgpt = chatgpt + 100000 WHERE user_id = '{user_id}'")
                await cursor.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
                await conn.commit()
    async def update_dalle(user_id: int, invoice_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET dall_e = dall_e + 100 WHERE user_id = '{user_id}'")
                await cursor.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
                await conn.commit()
    async def update_stable(user_id: int, invoice_id: int):
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET stable_diffusion = stable_diffusion + 100 WHERE user_id = '{user_id}'")
                await cursor.execute(f"DELETE FROM orders WHERE invoice_id = {invoice_id}")
                await conn.commit()