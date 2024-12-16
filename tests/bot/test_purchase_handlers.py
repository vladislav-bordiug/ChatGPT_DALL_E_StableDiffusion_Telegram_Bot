import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from app.bot.handlers.purchase_handlers import PurchaseHandlers
from app.bot.utils import States
from app.services.cryptopay import CryptoPayError
from app.services.db import DatabaseError

class TestBuyHandler:
    @pytest.mark.asyncio
    async def test_buy_handler_success(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "💲USD"

        state = AsyncMock(spec=FSMContext)
        state.get_state.return_value = States.PURCHASE_CHATGPT_STATE

        mock_db = AsyncMock()
        mock_crypto = AsyncMock()

        mock_crypto.create_invoice.return_value = 'sads', 12345

        handler = PurchaseHandlers(mock_db, mock_crypto)

        await handler.buy_handler(message, state)

        mock_db.new_order.assert_awaited_once_with(12345, 12345, 'chatgpt')
        mock_crypto.create_invoice.assert_awaited_once_with(5, 'USD')

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="💰Buy", url='sads')]]
        )
        message.answer.assert_awaited_once_with(
            text = "🪙Product: 100K ChatGPT tokens - 5 USD💵 \n 💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗Consider the network commission",
            reply_markup= keyboard,
        )

    @pytest.mark.asyncio
    async def test_buy_handler_database_error(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "💲USD"

        state = AsyncMock(spec=FSMContext)

        mock_db = AsyncMock()
        mock_crypto = AsyncMock()

        mock_crypto.create_invoice.side_effect = DatabaseError()

        handler = PurchaseHandlers(mock_db, mock_crypto)

        with pytest.raises(DatabaseError):
            await handler.buy_handler(message, state)

        mock_crypto.create_invoice.assert_awaited_once_with(5, 'USD')

    @pytest.mark.asyncio
    async def test_buy_handler_cryptopay_error(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "💲USD"

        state = AsyncMock(spec=FSMContext)

        mock_db = AsyncMock()
        mock_crypto = AsyncMock()

        mock_crypto.create_invoice.side_effect = CryptoPayError()

        handler = PurchaseHandlers(mock_db, mock_crypto)

        with pytest.raises(CryptoPayError):
            await handler.buy_handler(message, state)

        mock_crypto.create_invoice.assert_awaited_once_with(5, 'USD')

    @pytest.mark.asyncio
    async def test_buy_handler_telegram_error(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.answer.side_effect = Exception()
        message.from_user = MagicMock(id=12345)
        message.text = "💲USD"

        state = AsyncMock(spec=FSMContext)
        state.get_state.return_value = States.PURCHASE_CHATGPT_STATE

        mock_db = AsyncMock()
        mock_crypto = AsyncMock()

        mock_crypto.create_invoice.return_value = 'sads', 12345

        handler = PurchaseHandlers(mock_db, mock_crypto)

        with pytest.raises(Exception):
            await handler.buy_handler(message, state)

        mock_db.new_order.assert_awaited_once_with(12345, 12345, 'chatgpt')
        mock_crypto.create_invoice.assert_awaited_once_with(5, 'USD')

class TestCurrenciesHandler:
    @pytest.mark.asyncio
    async def test_currencies_handler_success(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.text = "100K ChatGPT tokens - 5 USD💵"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        handler = PurchaseHandlers(AsyncMock(), AsyncMock())

        await handler.currencies_handler(message, state)

        buttons = [
            [KeyboardButton(text="💲USDT"),
             KeyboardButton(text="💲TON")],
            [KeyboardButton(text="💲BTC"),
             KeyboardButton(text="💲ETH")],
            [KeyboardButton(text="🔙Back")]
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True
        )

        message.answer.assert_awaited_once_with(
            text = "Choose currency: 👇",
            reply_markup=keyboard,
        )

        state.set_state.assert_awaited_once_with(States.PURCHASE_CHATGPT_STATE)

    @pytest.mark.asyncio
    async def test_currencies_handler_telegram_error(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.answer.side_effect = Exception()
        message.text = "100K ChatGPT tokens - 5 USD💵"

        state = AsyncMock(spec=FSMContext)

        handler = PurchaseHandlers(AsyncMock(), AsyncMock())

        with pytest.raises(Exception):
            await handler.currencies_handler(message, state)

        buttons = [
            [KeyboardButton(text="💲USDT"),
             KeyboardButton(text="💲TON")],
            [KeyboardButton(text="💲BTC"),
             KeyboardButton(text="💲ETH")],
            [KeyboardButton(text="🔙Back")]
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True
        )

        message.answer.assert_awaited_once_with(
            text = "Choose currency: 👇",
            reply_markup=keyboard,
        )

class TestPurchaseHandler:
    @pytest.mark.asyncio
    async def test_purchase_handler_success(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        handler = PurchaseHandlers(AsyncMock(), AsyncMock())

        await handler.purchase_handler(message, state)

        button = [[KeyboardButton(text="100K ChatGPT tokens - 5 USD💵")],
                  [KeyboardButton(text="50 DALL·E image generations - 5 USD💵")],
                  [KeyboardButton(text="50 Stable Diffusion image generations - 5 USD💵")],
                  [KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer.assert_awaited_once_with(
            text = "Choose product: 👇",
            reply_markup= reply_markup,
        )
        state.set_state.assert_awaited_once_with(States.PURCHASE_STATE)

    @pytest.mark.asyncio
    async def test_purchase_handler_telegram_error(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.answer.side_effect = Exception()

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        handler = PurchaseHandlers(AsyncMock(), AsyncMock())

        with pytest.raises(Exception):
            await handler.purchase_handler(message, state)