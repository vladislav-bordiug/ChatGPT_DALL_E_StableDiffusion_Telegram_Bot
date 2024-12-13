from ..utils import States, translator

from openaitools import OpenAiTools

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update
from aiogram.fsm.context import FSMContext

from db import DataBase

async def dall_e_answer_handler(message: types.Message, state: FSMContext, database: DataBase, openai: OpenAiTools):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard = button, resize_keyboard=True
    )

    user_id = message.from_user.id
    result = await database.get_dalle(user_id)

    if result > 0:
        question = message.text

        prompt = await translator.translate(question, targetlang='en')

        answer = await openai.get_dalle(prompt.text)

        if answer:
            result -= 1
            await database.set_dalle(user_id, result)
            await message.answer_photo(
                photo=answer,
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
            text = "❎You have 0 DALL·E image generations. You need to buy them to use DALL·E.",
            reply_markup=reply_markup,
        )
    await state.set_state(States.DALL_E_STATE)