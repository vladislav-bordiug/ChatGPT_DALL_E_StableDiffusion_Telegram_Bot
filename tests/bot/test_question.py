import pytest
from unittest.mock import AsyncMock
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.bot.handlers.question import question_handler
from app.bot.utils import States

@pytest.mark.asyncio
async def test_question_handler_success():
    message = AsyncMock(spec=types.Message)
    message.text = "💭Chatting — ChatGPT-4o"
    message.answer = AsyncMock()

    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()

    await question_handler(message, state)

    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard=button, resize_keyboard=True
    )
    message.answer.assert_awaited_once_with(
        text = "Enter your text: 👇🏻",
        reply_markup= reply_markup,
    )
    state.set_state.assert_awaited_once_with(States.CHATGPT_STATE)

@pytest.mark.asyncio
async def test_question_handler_telegram_error():
    message = AsyncMock(spec=types.Message)
    message.text = "💭Chatting — ChatGPT-4o"
    message.answer = AsyncMock()
    message.answer.side_effect = Exception()

    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()

    with pytest.raises(Exception):
        await question_handler(message, state)