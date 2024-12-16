from app.bot.utils import States, translator, TelegramError, encoding

from app.services.stablediffusion import StableDiffusion
from app.services.openaitools import OpenAiTools

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile

from app.services.db import DataBase, DatabaseError

class AnswerHandlers:
    def __init__(self, database: DataBase, openai: OpenAiTools, stable: StableDiffusion):
        self.database = database
        self.openai = openai
        self.stable = stable

    async def chatgpt_answer_handler(self, message: types.Message, state: FSMContext):
        try:
            button = [[KeyboardButton(text="🔙Back")]]
            reply_markup = ReplyKeyboardMarkup(
                keyboard = button, resize_keyboard=True
            )

            user_id = message.from_user.id
            result = await self.database.get_chatgpt(user_id)

            if result > 0:
                await self.database.save_message(user_id, "user", message.text, len(encoding.encode(message.text)))

                messages, question_tokens = await self.database.get_messages(user_id)

                answer = await self.openai.get_chatgpt(messages)

                if answer:
                    answer_tokens = len(encoding.encode(answer))
                    await self.database.save_message(user_id, "assistant", answer, answer_tokens)

                    result -= int(question_tokens*0.25 + answer_tokens)

                    if result > 0:
                        await self.database.set_chatgpt(user_id, result)
                    else:
                        await self.database.set_chatgpt(user_id, 0)

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
        except DatabaseError:
            raise DatabaseError
        except Exception as e:
            err = TelegramError(str(e))
            err.output()
            raise err

    async def dall_e_answer_handler(self, message: types.Message, state: FSMContext):
        try:
            button = [[KeyboardButton(text="🔙Back")]]
            reply_markup = ReplyKeyboardMarkup(
                keyboard = button, resize_keyboard=True
            )

            user_id = message.from_user.id
            result = await self.database.get_dalle(user_id)

            if result > 0:
                question = message.text

                prompt = await translator.translate(question, targetlang='en')

                answer = await self.openai.get_dalle(prompt.text)

                if answer:
                    result -= 1
                    await self.database.set_dalle(user_id, result)
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
        except DatabaseError:
            raise DatabaseError
        except Exception as e:
            err = TelegramError(str(e))
            err.output()
            raise err

    async def stable_answer_handler(self, message: types, state: FSMContext):
        try:
            button = [[KeyboardButton(text="🔙Back")]]
            reply_markup = ReplyKeyboardMarkup(
                keyboard = button, resize_keyboard=True
            )

            user_id = message.from_user.id
            result = await self.database.get_stable(user_id)

            if result > 0:

                question = message.text

                prompt = await translator.translate(question, targetlang='en')

                photo = await self.stable.get_stable(prompt.text)

                if photo:
                    result -= 1
                    await self.database.set_stable(user_id, result)
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