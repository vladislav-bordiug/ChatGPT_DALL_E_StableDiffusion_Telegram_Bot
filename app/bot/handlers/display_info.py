from app.bot.utils import States, TelegramError

from aiogram import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from app.services.db import DataBase, DatabaseError

class DisplayInfo:
    def __init__(self, database: DataBase):
        self.database = database

    async def display_info_handler(self, message: types.Message, state: FSMContext):
        try:
            user_id = message.from_user.id
            result = await self.database.get_userinfo(user_id)

            button = [[KeyboardButton(text="💰Buy tokens and generations")], [KeyboardButton(text="🔙Back")]]
            reply_markup = ReplyKeyboardMarkup(
                keyboard = button, resize_keyboard=True
            )
            await message.answer(
                text = f"You have: \n 💭{result[0]} ChatGPT tokens \n 🌄{result[1]} DALL·E image generations \n 🌅{result[2]} Stable Diffusion image generations \n 💸 You can buy more with crypto",
                reply_markup=reply_markup,
            )
            await state.set_state(States.INFO_STATE)
        except DatabaseError:
            raise DatabaseError
        except Exception as e:
            err = TelegramError(str(e))
            err.output()
            raise err