import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.bot.handlers.start import StartHandler
from app.bot.utils import States
from app.services.db import DatabaseError

@pytest.mark.asyncio
async def test_start_handler_success_notuser():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    message.from_user = MagicMock(id=12345)

    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()

    mock_db = AsyncMock()
    mock_db.is_user.return_value = None

    handler = StartHandler(mock_db)

    await handler.start_handler(message, state)

    mock_db.delete_messages.assert_awaited_once_with(12345)

    mock_db.is_user.assert_awaited_once_with(12345)

    button = [[KeyboardButton(text="💭Chatting — ChatGPT-4o")],
              [KeyboardButton(text="🌄Image generation — DALL·E 3")],
              [KeyboardButton(text="🌅Image generation — Stable Diffusion 3")],
              [KeyboardButton(text="👤My account | 💰Buy")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard=button, resize_keyboard=True
    )
    message.answer.assert_awaited_once_with(
        text = "👋You have: \n💭3000 ChatGPT tokens \n🌄3 DALL·E Image generations \n🌅3 Stable Diffusion Image generations\n Choose an option: 👇 \n If buttons don't work, enter /start command",
        reply_markup= reply_markup,
    )
    state.set_state.assert_awaited_once_with(States.ENTRY_STATE)

@pytest.mark.asyncio
async def test_start_handler_success_isuser():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    message.from_user = MagicMock(id=12345)

    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()

    mock_db = AsyncMock()
    mock_db.is_user.return_value = 1

    handler = StartHandler(mock_db)

    await handler.start_handler(message, state)

    mock_db.delete_messages.assert_awaited_once_with(12345)

    mock_db.is_user.assert_awaited_once_with(12345)

    button = [[KeyboardButton(text="💭Chatting — ChatGPT-4o")],
              [KeyboardButton(text="🌄Image generation — DALL·E 3")],
              [KeyboardButton(text="🌅Image generation — Stable Diffusion 3")],
              [KeyboardButton(text="👤My account | 💰Buy")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard=button, resize_keyboard=True
    )
    message.answer.assert_awaited_once_with(
        text = "Choose an option: 👇🏻 \n If buttons don't work, enter /start command",
        reply_markup= reply_markup,
    )
    state.set_state.assert_awaited_once_with(States.ENTRY_STATE)

@pytest.mark.asyncio
async def test_start_handler_database_error():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    message.from_user = MagicMock(id=12345)

    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()

    mock_db = AsyncMock()
    mock_db.is_user.side_effect = DatabaseError()

    handler = StartHandler(mock_db)

    with pytest.raises(DatabaseError):
        await handler.start_handler(message, state)

@pytest.mark.asyncio
async def test_start_handler_telegram_error():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    message.answer.side_effect = Exception()
    message.from_user = MagicMock(id=12345)

    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()

    mock_db = AsyncMock()
    mock_db.is_user.return_value = None

    handler = StartHandler(mock_db)

    with pytest.raises(Exception):
        await handler.start_handler(message, state)

    mock_db.delete_messages.assert_awaited_once_with(12345)

    mock_db.is_user.assert_awaited_once_with(12345)