from ..utils import States, encoding

from app.services.openaitools import OpenAiTools

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from app.services.db import DataBase

async def chatgpt_answer_handler(message: types.Message, state: FSMContext, database: DataBase, openai: OpenAiTools):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard = button, resize_keyboard=True
    )

    user_id = message.from_user.id
    result = await database.get_chatgpt(user_id)

    if result > 0:
        await database.save_message(user_id, "user", message.text, len(encoding.encode(message.text)))

        messages, question_tokens = await database.get_messages(user_id)

        answer = await openai.get_chatgpt(messages)

        if answer:
            answer_tokens = len(encoding.encode(answer))
            await database.save_message(user_id, "assistant", answer, answer_tokens)

            result -= int(question_tokens*0.25 + answer_tokens)

            if result > 0:
                await database.set_chatgpt(user_id, result)
            else:
                await database.set_chatgpt(user_id, 0)

            await message.answer(
                text = answer,
                reply_markup=reply_markup,
            )
        else:
            await message.answer(
                text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )

    else:
        await message.answer(
            text = "❎You have 0 ChatGPT tokens. You need to buy them to use ChatGPT.",
            reply_markup=reply_markup,
        )
    await state.set_state(States.CHATGPT_STATE)