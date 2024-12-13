from ..utils import States, TelegramError

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update
from aiogram.fsm.context import FSMContext

async def currencies_handler(message: types.Message, state: FSMContext):
    try:
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
    except Exception as e:
        err = TelegramError(str(e))
        err.output()
        raise err