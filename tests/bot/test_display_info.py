import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.bot.handlers.display_info import DisplayInfo
from app.bot.utils import States
from app.services.db import DatabaseError

@pytest.mark.asyncio
async def test_display_info_handler_success():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    message.from_user = MagicMock(id=12345)

    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()

    mock_db = AsyncMock()
    mock_db.get_userinfo.return_value = [1, 1, 1]

    handler = DisplayInfo(mock_db)

    await handler.display_info_handler(message, state)

    mock_db.get_userinfo.assert_awaited_once_with(12345)

    button = [[KeyboardButton(text="💰Buy tokens and generations")], [KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard=button, resize_keyboard=True
    )
    message.answer.assert_awaited_once_with(
        text = "You have: \n 💭1 ChatGPT tokens \n 🌄1 DALL·E image generations \n 🌅1 Stable Diffusion image generations \n 💸 You can buy more with crypto",
        reply_markup= reply_markup,
    )
    state.set_state.assert_awaited_once_with(States.INFO_STATE)

@pytest.mark.asyncio
async def test_display_info_handler_database_error():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    message.from_user = MagicMock(id=12345)

    state = AsyncMock(spec=FSMContext)

    mock_db = AsyncMock()
    mock_db.get_userinfo.side_effect = DatabaseError()

    handler = DisplayInfo(mock_db)

    with pytest.raises(DatabaseError):
        await handler.display_info_handler(message, state)

@pytest.mark.asyncio
async def test_display_info_handler_telegram_error():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    message.answer.side_effect = Exception()
    message.from_user = MagicMock(id=12345)

    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()

    mock_db = AsyncMock()
    mock_db.get_userinfo.return_value = [1, 1, 1]

    handler = DisplayInfo(mock_db)

    with pytest.raises(Exception):
        await handler.display_info_handler(message, state)

    mock_db.get_userinfo.assert_awaited_once_with(12345)