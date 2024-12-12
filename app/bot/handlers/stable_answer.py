from ..utils import States, translator

from stablediffusion import StableDiffusion

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile

from db import DataBase

async def stable_answer_handler(message: types, state: FSMContext):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard = button, resize_keyboard=True
    )

    user_id = message.from_user.id
    result = await DataBase.get_stable(user_id)

    if result > 0:

        question = message.text

        prompt = await translator.translate(question, targetlang='en')

        photo = await StableDiffusion.get_stable(prompt.text)

        if photo:
            result -= 1
            await DataBase.set_stable(user_id, result)
            await message.answer_photo(
                photo=BufferedInputFile(photo, 'image.jpeg'),
                reply_markup=reply_markup,
                caption=question,
            )
        else:
            await message.answer(
                text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )
    else:
        await message.answer(
            text = "❎You have 0 Stable Diffusion image generations. You need to buy them to use Stable Diffusion.",
            reply_markup=reply_markup,
        )
    await state.set_state(States.STABLE_STATE)