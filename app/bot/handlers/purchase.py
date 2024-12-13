from ..utils import States, TelegramError

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update
from aiogram.fsm.context import FSMContext

async def purchase_handler(message: types.Message, state: FSMContext):
    try:
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
    except Exception as e:
        err = TelegramError(str(e))
        err.output()
        raise err