from ..utils import States

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from app.services.db import DataBase

async def display_info_handler(message: types.Message, state: FSMContext, database: DataBase):
    user_id = message.from_user.id
    result = await database.get_userinfo(user_id)

    button = [[KeyboardButton(text="💰Buy tokens and generations")], [KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard = button, resize_keyboard=True
    )
    await message.answer(
        text = f"You have: \n 💭{result[0]} ChatGPT tokens \n 🌄{result[1]} DALL·E image generations \n 🌅{result[2]} Stable Diffusion image generations \n 💸 You can buy more with crypto",
        reply_markup=reply_markup,
    )
    await state.set_state(States.INFO_STATE)