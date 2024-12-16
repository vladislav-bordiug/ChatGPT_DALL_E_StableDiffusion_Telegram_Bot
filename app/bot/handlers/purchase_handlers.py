from app.bot.utils import States, TelegramError

from app.services.cryptopay import CryptoPay, CryptoPayError

from aiogram import types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext

from app.services.db import DataBase, DatabaseError

class PurchaseHandlers:
    def __init__(self, database: DataBase, crypto: CryptoPay):
        self.database = database
        self.crypto = crypto

    async def buy_handler(self, message: types.Message, state: FSMContext):
        try:
            user_id = message.from_user.id
            currency = message.text
            invoice_url, invoice_id = await self.crypto.create_invoice(5, currency[1:])
            current_state = await state.get_state()
            product = ''
            if current_state == States.PURCHASE_CHATGPT_STATE:
                product = '100K ChatGPT tokens - 5 USD💵'
                await self.database.new_order(invoice_id, user_id, 'chatgpt')
            elif current_state == States.PURCHASE_DALL_E_STATE:
                product = '50 DALL·E image generations - 5 USD💵'
                await self.database.new_order(invoice_id, user_id, 'dall_e')
            elif current_state == States.PURCHASE_STABLE_STATE:
                product = '50 Stable Diffusion image generations - 5 USD💵'
                await self.database.new_order(invoice_id, user_id, 'stable')
            keyboard = InlineKeyboardMarkup(
                inline_keyboard = [[InlineKeyboardButton(text="💰Buy", url=invoice_url)]]
            )
            await message.answer(
                text = f"🪙Product: {product} \n 💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗Consider the network commission",
                reply_markup=keyboard,
            )
        except CryptoPayError:
            raise CryptoPayError
        except DatabaseError:
            raise DatabaseError
        except Exception as e:
            err = TelegramError(str(e))
            err.output()
            raise err

    async def currencies_handler(self, message: types.Message, state: FSMContext):
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

    async def purchase_handler(self, message: types.Message, state: FSMContext):
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