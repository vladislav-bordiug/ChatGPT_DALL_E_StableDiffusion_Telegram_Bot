from psycopg_pool import AsyncConnectionPool

class DataBaseCore:
    def __init__(self, conninfo: str):
        self.pool = AsyncConnectionPool(conninfo=conninfo, timeout = 10, max_lifetime=600, check=AsyncConnectionPool.check_connection, open = False)

    async def open_pool(self):
        await self.pool.open()
        await self.pool.wait()

    async def close_pool(self):
        if self.pool:
            await self.pool.close()