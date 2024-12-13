from ..utils import States, translator, TelegramError

from app.services.stablediffusion import StableDiffusion

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile

from app.services.db import DataBase, DatabaseError

async def stable_answer_handler(message: types, state: FSMContext, database: DataBase, stable: StableDiffusion):
    try:
        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard = button, resize_keyboard=True
        )

        user_id = message.from_user.id
        result = await database.get_stable(user_id)

        if result > 0:

            question = message.text

            prompt = await translator.translate(question, targetlang='en')

            photo = await stable.get_stable(prompt.text)

            if photo:
                result -= 1
                await database.set_stable(user_id, result)
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
    except DatabaseError:
        raise DatabaseError
    except Exception as e:
        err = TelegramError(str(e))
        err.output()
        raise err