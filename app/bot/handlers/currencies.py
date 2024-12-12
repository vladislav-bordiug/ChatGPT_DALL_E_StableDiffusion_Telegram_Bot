from ..utils import States

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update
from aiogram.fsm.context import FSMContext
from aiogram import F

@dp.message(States.PURCHASE_STATE, F.text.regexp(r'^100K ChatGPT tokens - 5 USD💵$'))
@dp.message(States.PURCHASE_STATE, F.text.regexp(r'^50 DALL·E image generations - 5 USD💵$'))
@dp.message(States.PURCHASE_STATE, F.text.regexp(r'^50 Stable Diffusion image generations - 5 USD💵$'))
async def currencies_handler(message: types.Message, state: FSMContext):
    buttons = [
        [KeyboardButton(text="💲USDT"),
        KeyboardButton(text="💲TON")],
        [KeyboardButton(text="💲BTC"),
        KeyboardButton(text="💲ETH")],
        [KeyboardButton(text="🔙Back")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard = buttons,
        resize_keyboard=True
    )
    await message.answer(
        text = "Choose currency: 👇",
        reply_markup=keyboard,
    )
    product = message.text
    if product == "100K ChatGPT tokens - 5 USD💵":
        await state.set_state(States.PURCHASE_CHATGPT_STATE)
    elif product == "50 DALL·E image generations - 5 USD💵":
        await state.set_state(States.PURCHASE_DALL_E_STATE)
    elif product == "50 Stable Diffusion image generations - 5 USD💵":
        await state.set_state(States.PURCHASE_STABLE_STATE)