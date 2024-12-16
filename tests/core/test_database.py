import pytest
from unittest.mock import AsyncMock

from app.core.database import DataBaseCore

class TestOpenPool:
    @pytest.mark.asyncio
    async def test_open_pool_success(self):
        dbcore = DataBaseCore('conninfo')
        dbcore.pool = AsyncMock()

        await dbcore.open_pool()

        dbcore.pool.open.assert_awaited_once_with()
        dbcore.pool.wait.assert_awaited_once_with()

class TestClosePool:
    @pytest.mark.asyncio
    async def test_open_pool_success(self):
        dbcore = DataBaseCore('conninfo')
        dbcore.pool = AsyncMock()

        await dbcore.close_pool()

        dbcore.pool.close.assert_awaited_once_with()