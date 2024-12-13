from ..utils import States

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update
from aiogram.fsm.context import FSMContext

from db import DataBase

async def start_handler(message: types.Message, state: FSMContext, database: DataBase):
    user_id = message.from_user.id
    result = await database.is_user(user_id)
    button = [[KeyboardButton(text="💭Chatting — ChatGPT-4o")],
              [KeyboardButton(text="🌄Image generation — DALL·E 3")],
              [KeyboardButton(text="🌅Image generation — Stable Diffusion 3")],
              [KeyboardButton(text="👤My account | 💰Buy")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard = button, resize_keyboard=True
    )
    await database.delete_messages(user_id)
    if not result:
        await database.insert_user(user_id)
        await message.answer(
            text = "👋You have: \n💭3000 ChatGPT tokens \n🌄3 DALL·E Image generations \n🌅3 Stable Diffusion Image generations\n Choose an option: 👇 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )
    else:
        await message.answer(
            text = "Choose an option: 👇🏻 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )
    await state.set_state(States.ENTRY_STATE)