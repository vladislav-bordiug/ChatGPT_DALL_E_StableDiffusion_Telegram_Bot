from ..utils import States

from app.services.cryptopay import CryptoPay

from aiogram import types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from app.services.db import DataBase

async def buy_handler(message: types.Message, state: FSMContext, database: DataBase, crypto: CryptoPay):
    user_id = message.from_user.id
    currency = message.text
    invoice_url, invoice_id = await crypto.create_invoice(5, currency[1:])
    current_state = await state.get_state()
    product = ''
    if current_state == States.PURCHASE_CHATGPT_STATE:
        product = '100K ChatGPT tokens - 5 USD💵'
        await database.new_order(invoice_id, user_id, 'chatgpt')
    elif current_state == States.PURCHASE_DALL_E_STATE:
        product = '50 DALL·E image generations - 5 USD💵'
        await database.new_order(invoice_id, user_id, 'dall_e')
    elif current_state == States.PURCHASE_STABLE_STATE:
        product = '50 Stable Diffusion image generations - 5 USD💵'
        await database.new_order(invoice_id, user_id, 'stable')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [[InlineKeyboardButton(text="💰Buy", url=invoice_url)]]
    )
    await message.answer(
        text = f"🪙Product: {product} \n 💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗Consider the network commission",
        reply_markup=keyboard,
    )