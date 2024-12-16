import pytest
from unittest.mock import AsyncMock, patch
from fastapi import Request
import json

from app.api.routes.routes import Handlers
from app.bot.utils import TelegramError
from app.services.cryptopay import CryptoPayError
from app.services.db import DatabaseError

from aiogram import types

class TestPaymentsWebhookHandler:
    @patch('app.api.routes.routes.payment_success', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_payments_webhook_success(self, mock_payment_success):

        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"update_type": "invoice_paid", "payload": {"invoice_id": "1"}}

        mock_bot = AsyncMock()
        mock_db = AsyncMock()

        handler = Handlers(mock_db, AsyncMock(), mock_bot)

        response = await handler.payments_webhook(mock_request)

        assert response.body.decode('utf-8') == "OK"
        assert response.status_code == 200

        mock_payment_success.assert_awaited_once_with(mock_bot, mock_db, "invoice_paid", 1)

    @pytest.mark.asyncio
    async def test_payments_webhook_request_error(self):

        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"payload": {"invoice_id": "1"}}

        mock_bot = AsyncMock()
        mock_db = AsyncMock()

        handler = Handlers(mock_db, AsyncMock(), mock_bot)

        response = await handler.payments_webhook(mock_request)

        assert response.body.decode('utf-8') == "Wrong request"
        assert response.status_code == 400

    @patch('app.api.routes.routes.payment_success', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_payments_webhook_database_error(self, mock_payment_success):

        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"update_type": "invoice_paid", "payload": {"invoice_id": "1"}}

        mock_bot = AsyncMock()
        mock_db = AsyncMock()

        mock_payment_success.side_effect = DatabaseError()

        handler = Handlers(mock_db, AsyncMock(), mock_bot)

        response = await handler.payments_webhook(mock_request)

        assert response.body.decode('utf-8') == "Database Error"
        assert response.status_code == 500

        mock_payment_success.assert_awaited_once_with(mock_bot, mock_db, "invoice_paid", 1)


    @patch('app.api.routes.routes.payment_success', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_payments_webhook_telegram_error(self, mock_payment_success):
        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"update_type": "invoice_paid", "payload": {"invoice_id": "1"}}

        mock_bot = AsyncMock()
        mock_db = AsyncMock()

        mock_payment_success.side_effect = TelegramError()

        handler = Handlers(mock_db, AsyncMock(), mock_bot)

        response = await handler.payments_webhook(mock_request)

        assert response.body.decode('utf-8') == "Telegram Error"
        assert response.status_code == 500

        mock_payment_success.assert_awaited_once_with(mock_bot, mock_db, "invoice_paid", 1)

    @patch('app.api.routes.routes.payment_success', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_payments_webhook_general_error(self, mock_payment_success):
        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"update_type": "invoice_paid", "payload": {"invoice_id": "1"}}

        mock_bot = AsyncMock()
        mock_db = AsyncMock()

        mock_payment_success.side_effect = Exception()

        handler = Handlers(mock_db, AsyncMock(), mock_bot)

        response = await handler.payments_webhook(mock_request)

        assert response.body.decode('utf-8') == "Error"
        assert response.status_code == 500

        mock_payment_success.assert_awaited_once_with(mock_bot, mock_db, "invoice_paid", 1)

class TestBotWebhookHandler:
    @pytest.mark.asyncio
    async def test_bot_webhook_success(self):

        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"update_id": 12345}

        mock_dp = AsyncMock()
        mock_bot = AsyncMock()

        handler = Handlers(AsyncMock(), mock_dp, mock_bot)

        response = await handler.bot_webhook(mock_request)

        assert response.status_code == 200
        assert json.loads(response.body.decode('utf-8')) == {"status": "ok"}
        mock_dp.feed_webhook_update.assert_awaited_once_with(mock_bot, types.Update(update_id=12345))

    @pytest.mark.asyncio
    async def test_bot_webhook_request_error(self):
        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {}

        mock_dp = AsyncMock()
        mock_bot = AsyncMock()

        handler = Handlers(AsyncMock(), mock_dp, mock_bot)

        response = await handler.bot_webhook(mock_request)

        assert response.status_code == 400
        assert json.loads(response.body.decode('utf-8')) == {"message": "Wrong request"}

    @pytest.mark.asyncio
    async def test_bot_webhook_database_error(self):

        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"update_id": 12345}

        mock_dp = AsyncMock()
        mock_bot = AsyncMock()

        mock_dp.feed_webhook_update.side_effect = DatabaseError()

        handler = Handlers(AsyncMock(), mock_dp, mock_bot)

        response = await handler.bot_webhook(mock_request)

        assert response.status_code == 500
        assert json.loads(response.body.decode('utf-8')) == {"message": "database error"}


    @pytest.mark.asyncio
    async def test_bot_webhook_cryptopay_error(self):

        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"update_id": 12345}

        mock_dp = AsyncMock()
        mock_bot = AsyncMock()

        mock_dp.feed_webhook_update.side_effect = CryptoPayError()

        handler = Handlers(AsyncMock(), mock_dp, mock_bot)

        response = await handler.bot_webhook(mock_request)

        assert response.status_code == 500
        assert json.loads(response.body.decode('utf-8')) == {"message": "cryptopay error"}


    @pytest.mark.asyncio
    async def test_bot_webhook_telegram_error(self):

        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"update_id": 12345}

        mock_dp = AsyncMock()
        mock_bot = AsyncMock()

        mock_dp.feed_webhook_update.side_effect = TelegramError()

        handler = Handlers(AsyncMock(), mock_dp, mock_bot)

        response = await handler.bot_webhook(mock_request)

        assert response.status_code == 500
        assert json.loads(response.body.decode('utf-8')) == {"message": "telegram error"}


    @pytest.mark.asyncio
    async def test_bot_webhook_general_error(self):

        mock_request = AsyncMock(spec=Request)
        mock_request.json.return_value = {"update_id": 12345}

        mock_dp = AsyncMock()
        mock_bot = AsyncMock()

        mock_dp.feed_webhook_update.side_effect = Exception()

        handler = Handlers(AsyncMock(), mock_dp, mock_bot)

        response = await handler.bot_webhook(mock_request)

        assert response.status_code == 500
        assert json.loads(response.body.decode('utf-8')) == {"message": "error"}