import pytest
from unittest.mock import AsyncMock, MagicMock, call

from app.services.db import DataBase

class AsyncContextManager:
    def __init__(self):
        self.commit = AsyncMock()
        self.execute = AsyncMock()
        self.cursor = MagicMock()
        self.fetchone = AsyncMock()
        self.fetchall = AsyncMock()

    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, traceback):
        pass

class TestCreateTables:
    @pytest.mark.asyncio
    async def test_create_tables_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.create_tables()

        mock_connection.commit.assert_awaited_once_with()

        mock_cursor.execute.assert_has_calls([call("CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY, chatgpt INT, dall_e INT, stable_diffusion INT)"),
                                              call("CREATE TABLE IF NOT EXISTS orders (invoice_id INT PRIMARY KEY, user_id BIGINT, product TEXT, FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE)"),
                                              call("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, user_id BIGINT, role TEXT, content TEXT, tokens INT, FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE)")])
        assert len(mock_cursor.execute.mock_calls) == 3

    @pytest.mark.asyncio
    async def test_create_tables_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()
        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()

        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.create_tables()

        mock_connection.commit.assert_awaited_once_with()

        mock_cursor.execute.assert_has_calls([call("CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY, chatgpt INT, dall_e INT, stable_diffusion INT)"),
                                              call("CREATE TABLE IF NOT EXISTS orders (invoice_id INT PRIMARY KEY, user_id BIGINT, product TEXT, FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE)"),
                                              call("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, user_id BIGINT, role TEXT, content TEXT, tokens INT, FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE)")])
        assert len(mock_cursor.execute.mock_calls) == 3

class TestIsUser:
    @pytest.mark.asyncio
    async def test_is_user_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        mock_cursor.fetchone.return_value = (1)

        result = await database.is_user(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT user_id FROM users WHERE user_id = %s", (1, ))

        mock_cursor.fetchone.assert_awaited_once_with()

        assert result == (1)

    @pytest.mark.asyncio
    async def test_is_user_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.side_effect = Exception()

        database.pool.connection.return_value = mock_connection

        mock_cursor.execute.return_value = (1)

        with pytest.raises(Exception):
            _ = await database.is_user(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT user_id FROM users WHERE user_id = %s", (1,))

        mock_cursor.fetchone.assert_awaited_once_with()

class TestInsertUser:
    @pytest.mark.asyncio
    async def test_insert_user_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.insert_user(1)

        mock_cursor.execute.assert_awaited_once_with("INSERT INTO users(user_id, chatgpt, dall_e, stable_diffusion) VALUES (%s, %s, %s, %s)", (1,3000,3,3))

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_insert_user_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.insert_user(1)

        mock_cursor.execute.assert_awaited_once_with(
            "INSERT INTO users(user_id, chatgpt, dall_e, stable_diffusion) VALUES (%s, %s, %s, %s)", (1, 3000, 3, 3))

        mock_connection.commit.assert_awaited_once_with()

class TestGetChatgpt:
    @pytest.mark.asyncio
    async def test_get_chatgpt_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1,)

        database.pool.connection.return_value = mock_connection

        result = await database.get_chatgpt(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT chatgpt FROM users WHERE user_id = %s", (1, ))

        mock_cursor.fetchone.assert_awaited_once_with()

        assert result == 1

    @pytest.mark.asyncio
    async def test_get_chatgpt_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.side_effect = Exception()

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            _ = await database.get_chatgpt(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT chatgpt FROM users WHERE user_id = %s", (1,))

        mock_cursor.fetchone.assert_awaited_once_with()

class TestSetChatgpt:
    @pytest.mark.asyncio
    async def test_set_chatgpt_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.set_chatgpt(1,1)

        mock_cursor.execute.assert_awaited_once_with("UPDATE users SET chatgpt = %s WHERE user_id = %s", (1, 1))

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_set_chatgpt_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.set_chatgpt(1,1)

        mock_cursor.execute.assert_awaited_once_with("UPDATE users SET chatgpt = %s WHERE user_id = %s", (1, 1))

        mock_connection.commit.assert_awaited_once_with()

class TestGetDallE:
    @pytest.mark.asyncio
    async def test_get_dalle_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1,)

        database.pool.connection.return_value = mock_connection

        result = await database.get_dalle(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT dall_e FROM users WHERE user_id = %s", (1, ))

        mock_cursor.fetchone.assert_awaited_once_with()

        assert result == 1

    @pytest.mark.asyncio
    async def test_get_dalle_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.side_effect = Exception()

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            _ = await database.get_dalle(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT dall_e FROM users WHERE user_id = %s", (1,))

        mock_cursor.fetchone.assert_awaited_once_with()

class TestSetDallE:
    @pytest.mark.asyncio
    async def test_set_dalle_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.set_dalle(1,1)

        mock_cursor.execute.assert_awaited_once_with("UPDATE users SET dall_e = %s WHERE user_id = %s", (1, 1))

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_set_dalle_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.set_dalle(1,1)

        mock_cursor.execute.assert_awaited_once_with("UPDATE users SET dall_e = %s WHERE user_id = %s", (1, 1))

        mock_connection.commit.assert_awaited_once_with()

class TestGetStable:
    @pytest.mark.asyncio
    async def test_get_stable_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1,)

        database.pool.connection.return_value = mock_connection

        result = await database.get_stable(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT stable_diffusion FROM users WHERE user_id = %s", (1, ))

        mock_cursor.fetchone.assert_awaited_once_with()

        assert result == 1

    @pytest.mark.asyncio
    async def test_get_stable_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.side_effect = Exception()

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            _ = await database.get_stable(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT stable_diffusion FROM users WHERE user_id = %s", (1,))

        mock_cursor.fetchone.assert_awaited_once_with()

class TestSetStable:
    @pytest.mark.asyncio
    async def test_set_stable_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.set_stable(1,1)

        mock_cursor.execute.assert_awaited_once_with("UPDATE users SET stable_diffusion = %s WHERE user_id = %s", (1, 1))

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_set_stable_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.set_stable(1,1)

        mock_cursor.execute.assert_awaited_once_with("UPDATE users SET stable_diffusion = %s WHERE user_id = %s", (1, 1))

        mock_connection.commit.assert_awaited_once_with()

class TestGetUserinfo:
    @pytest.mark.asyncio
    async def test_get_userinfo_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1,1,1)

        database.pool.connection.return_value = mock_connection

        result = await database.get_userinfo(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT chatgpt, dall_e, stable_diffusion FROM users WHERE user_id = %s", (1, ))

        mock_cursor.fetchone.assert_awaited_once_with()

        assert result == (1,1,1)

    @pytest.mark.asyncio
    async def test_get_userinfo_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.side_effect = Exception()

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            _ = await database.get_userinfo(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT chatgpt, dall_e, stable_diffusion FROM users WHERE user_id = %s", (1,))

        mock_cursor.fetchone.assert_awaited_once_with()

class TestNewOrder:
    @pytest.mark.asyncio
    async def test_new_order_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.new_order(1,1, 'chatgpt')

        mock_cursor.execute.assert_awaited_once_with("INSERT INTO orders(invoice_id, user_id, product) VALUES (%s, %s, %s)", (1, 1, 'chatgpt'))

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_new_order_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.new_order(1,1, 'chatgpt')

        mock_cursor.execute.assert_awaited_once_with("INSERT INTO orders(invoice_id, user_id, product) VALUES (%s, %s, %s)", (1, 1, 'chatgpt'))

        mock_connection.commit.assert_awaited_once_with()

class TestGetOrderdata:
    @pytest.mark.asyncio
    async def test_get_orderdata_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1,'chatgpt')

        database.pool.connection.return_value = mock_connection

        result = await database.get_orderdata(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT user_id, product FROM orders WHERE invoice_id = %s", (1, ))

        mock_cursor.fetchone.assert_awaited_once_with()

        assert result == (1,'chatgpt')

    @pytest.mark.asyncio
    async def test_get_orderdata_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.side_effect = Exception()

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            _ = await database.get_orderdata(1)

        mock_cursor.execute.assert_awaited_once_with("SELECT user_id, product FROM orders WHERE invoice_id = %s", (1, ))

        mock_cursor.fetchone.assert_awaited_once_with()

class TestUpdateChatgpt:
    @pytest.mark.asyncio
    async def test_update_chatgpt_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.update_chatgpt(1,1)

        mock_cursor.execute.assert_has_calls([call("UPDATE users SET chatgpt = chatgpt + 100000 WHERE user_id = %s", (1, )),
                                              call("DELETE FROM orders WHERE invoice_id = %s", (1, ))])
        assert len(mock_cursor.execute.mock_calls) == 2

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_update_chatgpt_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.update_chatgpt(1,1)

        mock_cursor.execute.assert_has_calls([call("UPDATE users SET chatgpt = chatgpt + 100000 WHERE user_id = %s", (1, )),
                                              call("DELETE FROM orders WHERE invoice_id = %s", (1, ))])

        assert len(mock_cursor.execute.mock_calls) == 2

        mock_connection.commit.assert_awaited_once_with()

class TestUpdateDallE:
    @pytest.mark.asyncio
    async def test_update_dalle_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.update_dalle(1,1)

        mock_cursor.execute.assert_has_calls([call("UPDATE users SET dall_e = dall_e + 50 WHERE user_id = %s", (1, )),
                                              call("DELETE FROM orders WHERE invoice_id = %s", (1, ))])
        assert len(mock_cursor.execute.mock_calls) == 2

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_update_dalle_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.update_dalle(1,1)

        mock_cursor.execute.assert_has_calls([call("UPDATE users SET dall_e = dall_e + 50 WHERE user_id = %s", (1,)),
                                              call("DELETE FROM orders WHERE invoice_id = %s", (1,))])
        assert len(mock_cursor.execute.mock_calls) == 2

        mock_connection.commit.assert_awaited_once_with()

class TestUpdateStable:
    @pytest.mark.asyncio
    async def test_update_stable_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.update_stable(1,1)

        mock_cursor.execute.assert_has_calls([call("UPDATE users SET stable_diffusion = stable_diffusion + 50 WHERE user_id = %s", (1, )),
                                              call("DELETE FROM orders WHERE invoice_id = %s", (1, ))])
        assert len(mock_cursor.execute.mock_calls) == 2

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_update_stable_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.update_stable(1,1)

        mock_cursor.execute.assert_has_calls(
            [call("UPDATE users SET stable_diffusion = stable_diffusion + 50 WHERE user_id = %s", (1,)),
             call("DELETE FROM orders WHERE invoice_id = %s", (1,))])
        assert len(mock_cursor.execute.mock_calls) == 2

        mock_connection.commit.assert_awaited_once_with()

class TestSaveMessage:
    @pytest.mark.asyncio
    async def test_save_message_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.save_message(1,'user', 'message', 1)

        mock_cursor.execute.assert_awaited_once_with("INSERT INTO messages(user_id, role, content, tokens) VALUES (%s, %s, %s, %s)", (1,'user', 'message', 1))

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_save_message_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.save_message(1,'user', 'message', 1)

        mock_cursor.execute.assert_awaited_once_with("INSERT INTO messages(user_id, role, content, tokens) VALUES (%s, %s, %s, %s)", (1,'user', 'message', 1))

        mock_connection.commit.assert_awaited_once_with()

class TestDeleteMessages:
    @pytest.mark.asyncio
    async def test_delete_messages_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        await database.delete_messages(1)

        mock_cursor.execute.assert_awaited_once_with("DELETE FROM messages WHERE user_id = %s", (1,))

        mock_connection.commit.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_delete_messages_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_connection.commit.side_effect = Exception()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            await database.delete_messages(1)

        mock_cursor.execute.assert_awaited_once_with("DELETE FROM messages WHERE user_id = %s", (1,))

        mock_connection.commit.assert_awaited_once_with()

class TestGetMessages:
    @pytest.mark.asyncio
    async def test_get_messages_success(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [("user","message",1)]

        database.pool.connection.return_value = mock_connection

        result = await database.get_messages(1)

        mock_cursor.execute.assert_awaited_once_with("""
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
                    ORDER BY id ASC;""", (1,))

        mock_cursor.fetchall.assert_awaited_once_with()

        assert result == ([{'role': 'user', 'content': 'message'}], 1)

    @pytest.mark.asyncio
    async def test_get_messages_database_error(self):
        database = DataBase(AsyncMock())

        database.pool = MagicMock()

        mock_connection = AsyncContextManager()

        mock_cursor = AsyncContextManager()
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchall.side_effect = Exception()

        database.pool.connection.return_value = mock_connection

        with pytest.raises(Exception):
            _ = await database.get_messages(1)

        mock_cursor.execute.assert_awaited_once_with("""
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
                    ORDER BY id ASC;""", (1,))

        mock_cursor.fetchall.assert_awaited_once_with()