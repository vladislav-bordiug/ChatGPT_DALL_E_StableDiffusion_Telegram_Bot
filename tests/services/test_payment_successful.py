import pytest
from unittest.mock import AsyncMock

from app.services.payment_successful import payment_success

from app.services.db import DatabaseError

@pytest.mark.asyncio
async def test_payment_success_success():
    mock_bot = AsyncMock()
    mock_db = AsyncMock()

    update_type = "invoice_paid"

    invoice_id = 1

    mock_db.get_orderdata.return_value = (1, 'chatgpt')

    await payment_success(mock_bot, mock_db, update_type, invoice_id)

    mock_db.get_orderdata.assert_awaited_once_with(1)

    mock_db.update_chatgpt.assert_awaited_once_with(1, 1)

    mock_bot.send_message.assert_awaited_once_with(1, "✅You have received 100000 ChatGPT tokens!")

@pytest.mark.asyncio
async def test_payment_success_database_error():
    mock_bot = AsyncMock()
    mock_db = AsyncMock()

    update_type = "invoice_paid"

    invoice_id = 1

    mock_db.get_orderdata.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        await payment_success(mock_bot, mock_db, update_type, invoice_id)

    mock_db.get_orderdata.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_payment_success_telegram_error():
    mock_bot = AsyncMock()
    mock_db = AsyncMock()

    update_type = "invoice_paid"

    invoice_id = 1

    mock_db.get_orderdata.return_value = (1, 'dall_e')

    mock_bot.send_message.side_effect = Exception()

    with pytest.raises(Exception):
        await payment_success(mock_bot, mock_db, update_type, invoice_id)

    mock_db.get_orderdata.assert_awaited_once_with(1)

    mock_db.update_dalle.assert_awaited_once_with(1, 1)

    mock_bot.send_message.assert_awaited_once_with(1, "✅You have received 50 DALL·E image generations!")