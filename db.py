import asyncpg
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class DataBase:

    async def is_user(user_id: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        result = await conn.fetchval("SELECT user_id FROM users WHERE user_id = $1", user_id)
        await conn.close()
        return result

    async def insert_user(user_id: int, username: str):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        await conn.execute("INSERT INTO users(user_id, username, chatgpt, dall_e, stable_diffusion) VALUES ($1, $2, $3, $4, $5)", user_id,username,3000,3,3)
        await conn.close()

    async def get_chatgpt(user_id: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        result = await conn.fetchval("SELECT chatgpt FROM users WHERE user_id = $1", user_id)
        await conn.close()
        return result

    async def set_chatgpt(user_id: int, result: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        await conn.execute("UPDATE users SET chatgpt = $1 WHERE user_id = $2", result, user_id)
        await conn.close()

    async def get_dalle(user_id: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        result = await conn.fetchval("SELECT dall_e FROM users WHERE user_id = $1", user_id)
        await conn.close()
        return result

    async def set_dalle(user_id: int, result: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        await conn.execute("UPDATE users SET dall_e = $1 WHERE user_id = $2", result, user_id)
        await conn.close()

    async def get_stable(user_id: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        result = await conn.fetchval("SELECT stable_diffusion FROM users WHERE user_id = $1", user_id)
        await conn.close()
        return result

    async def set_stable(user_id: int, result: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        await conn.execute("UPDATE users SET stable_diffusion = $1 WHERE user_id = $2", result, user_id)
        await conn.close()

    async def get_userinfo(user_id: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        result = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
        await conn.close()
        return result

    async def new_order(invoice_id: int, user_id: int, product: str):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        await conn.execute("INSERT INTO orders(invoice_id, user_id, product) VALUES ($1, $2, $3)", invoice_id, user_id, product)
        await conn.close()

    async def get_orderdata(invoice_id: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        result = await conn.fetchrow("SELECT user_id, product FROM orders WHERE invoice_id = $1", invoice_id)
        await conn.close()
        return result

    async def update_chatgpt(user_id: int, invoice_id: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        await conn.execute("UPDATE users SET chatgpt = chatgpt + 100000 WHERE user_id = $1", user_id)
        await conn.execute("DELETE FROM orders WHERE invoice_id = $1", invoice_id)
        await conn.close()

    async def update_dalle(user_id: int, invoice_id: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        await conn.execute("UPDATE users SET dall_e = dall_e + 100 WHERE user_id = $1", user_id)
        await conn.execute("DELETE FROM orders WHERE invoice_id = $1", invoice_id)
        await conn.close()

    async def update_stable(user_id: int, invoice_id: int):
        conn = await asyncpg.connect(getenv("DATABASE_URL"))
        await conn.execute("UPDATE users SET stable_diffusion = stable_diffusion + 100 WHERE user_id = $1", user_id)
        await conn.execute("DELETE FROM orders WHERE invoice_id = $1", invoice_id)
        await conn.close()