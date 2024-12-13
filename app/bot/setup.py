from aiogram import Dispatcher
from app.bot.handlers.chatgpt_answer import chatgpt_answer_handler
from app.bot.handlers.currencies import currencies_handler
from app.bot.handlers.dall_e_answer import dall_e_answer_handler
from app.bot.handlers.display_info import display_info_handler
from app.bot.handlers.question import question_handler
from app.bot.handlers.stable_answer import stable_answer_handler
from app.bot.handlers.purchase import purchase_handler
from app.bot.handlers.start import start_handler
from app.bot.handlers.buy import buy_handler

from aiogram.filters.command import Command
from app.bot.utils import States
from aiogram import F
from aiogram import types
from aiogram.fsm.context import FSMContext

from openaitools import OpenAiTools
from db import DataBase
from stablediffusion import StableDiffusion
from cryptopay import CryptoPay

def register_handlers(dp: Dispatcher, database: DataBase, openai: OpenAiTools, stable: StableDiffusion, crypto: CryptoPay):
    register_purchase_handlers(dp, database, crypto)

    register_start_handlers(dp, database)

    register_question_handlers(dp)

    register_display_info_handlers(dp, database)

    register_answer_handlers(dp, database, openai, stable)

def register_purchase_handlers(dp: Dispatcher, database: DataBase, crypto: CryptoPay):
    dp.message.register(purchase_handler, States.INFO_STATE, F.text.regexp(r'^💰Buy tokens and generations$'))
    dp.message.register(purchase_handler, States.PURCHASE_CHATGPT_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(purchase_handler,States.PURCHASE_DALL_E_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(purchase_handler, States.PURCHASE_STABLE_STATE, F.text.regexp(r'^🔙Back$'))

    async def buy_handle(message: types.Message, state: FSMContext):
        return await buy_handler(message, state, database, crypto)
    currencies = ['USDT', 'TON', 'BTC', 'ETH']
    for currency in currencies:
        dp.message.register(buy_handle, States.PURCHASE_CHATGPT_STATE, F.text.regexp(rf'^💲{currency}$'))
        dp.message.register(buy_handle, States.PURCHASE_DALL_E_STATE, F.text.regexp(rf'^💲{currency}$'))
        dp.message.register(buy_handle, States.PURCHASE_STABLE_STATE, F.text.regexp(rf'^💲{currency}$'))

def register_start_handlers(dp: Dispatcher, database: DataBase):
    async def start_handle(message: types.Message, state: FSMContext):
        return await start_handler(message, state, database)
    dp.message.register(start_handle, Command('start'))
    dp.message.register(start_handle, States.ENTRY_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(start_handle, States.CHATGPT_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(start_handle, States.DALL_E_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(start_handle, States.STABLE_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(start_handle, States.INFO_STATE, F.text.regexp(r'^🔙Back$'))

def register_question_handlers(dp: Dispatcher):
    dp.message.register(question_handler, States.ENTRY_STATE, F.text.regexp(r'^💭Chatting — ChatGPT-4o$'))
    dp.message.register(question_handler, States.ENTRY_STATE, F.text.regexp(r'^🌄Image generation — DALL·E 3$'))
    dp.message.register(question_handler, States.ENTRY_STATE, F.text.regexp(r'^🌅Image generation — Stable Diffusion 3$'))

def register_display_info_handlers(dp: Dispatcher, database: DataBase):
    async def display_info_handle(message: types.Message, state: FSMContext):
        return await display_info_handler(message, state, database)
    dp.message.register(display_info_handle, States.ENTRY_STATE, F.text.regexp(r'^👤My account | 💰Buy$'))
    dp.message.register(display_info_handle, States.PURCHASE_STATE, F.text.regexp(r'^🔙Back$'))

def register_answer_handlers(dp: Dispatcher, database: DataBase, openai: OpenAiTools, stable: StableDiffusion):
    async def chatgpt_answer_handle(message: types.Message, state: FSMContext):
        return await chatgpt_answer_handler(message, state, database, openai)
    dp.message.register(chatgpt_answer_handle, States.CHATGPT_STATE, F.text)
    async def stable_answer_handle(message: types.Message, state: FSMContext):
        return await stable_answer_handler(message, state, database, stable)
    dp.message.register(stable_answer_handle, States.STABLE_STATE, F.text)
    async def dall_e_answer_handle(message: types.Message, state: FSMContext):
        return await dall_e_answer_handler(message, state, database, openai)
    dp.message.register(dall_e_answer_handle, States.DALL_E_STATE, F.text)
    dp.message.register(currencies_handler, States.PURCHASE_STATE, F.text.regexp(r'^100K ChatGPT tokens - 5 USD💵$'))
    dp.message.register(currencies_handler, States.PURCHASE_STATE, F.text.regexp(r'^50 DALL·E image generations - 5 USD💵$'))
    dp.message.register(currencies_handler, States.PURCHASE_STATE, F.text.regexp(r'^50 Stable Diffusion image generations - 5 USD💵$'))
