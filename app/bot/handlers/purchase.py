from ..utils import States

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot import dp

@dp.message(States.INFO_STATE, F.text.regexp(r'^💰Buy tokens and generations$'))
@dp.message(States.PURCHASE_CHATGPT_STATE, F.text.regexp(r'^🔙Back$'))
@dp.message(States.PURCHASE_DALL_E_STATE, F.text.regexp(r'^🔙Back$'))
@dp.message(States.PURCHASE_STABLE_STATE, F.text.regexp(r'^🔙Back$'))
async def purchase_handler(message: types.Message, state: FSMContext):
    button = [[KeyboardButton(text="100K ChatGPT tokens - 5 USD💵")],
              [KeyboardButton(text="50 DALL·E image generations - 5 USD💵")],
              [KeyboardButton(text="50 Stable Diffusion image generations - 5 USD💵")],
              [KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard = button, resize_keyboard=True
    )
    await message.answer(
        text = "Choose product: 👇",
        reply_markup=reply_markup,
    )
    await state.set_state(States.PURCHASE_STATE)