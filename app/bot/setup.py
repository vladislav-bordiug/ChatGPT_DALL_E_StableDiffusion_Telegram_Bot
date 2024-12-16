from aiogram import Dispatcher

from app.bot.handlers.answer_handlers import AnswerHandlers
from app.bot.handlers.display_info import DisplayInfo
from app.bot.handlers.purchase_handlers import PurchaseHandlers
from app.bot.handlers.question import question_handler
from app.bot.handlers.start import StartHandler

from aiogram.filters.command import Command
from app.bot.utils import States
from aiogram import F

from app.services.openaitools import OpenAiTools
from app.services.db import DataBase
from app.services.stablediffusion import StableDiffusion
from app.services.cryptopay import CryptoPay

def register_handlers(dp: Dispatcher, database: DataBase, openai: OpenAiTools, stable: StableDiffusion, crypto: CryptoPay):
    register_purchase_handlers(dp, database, crypto)

    register_start_handlers(dp, database)

    register_question_handlers(dp)

    register_display_info_handlers(dp, database)

    register_answer_handlers(dp, database, openai, stable)

def register_purchase_handlers(dp: Dispatcher, database: DataBase, crypto: CryptoPay):
    Purchase_Handlers = PurchaseHandlers(database, crypto)

    dp.message.register(Purchase_Handlers.purchase_handler, States.INFO_STATE, F.text.regexp(r'^💰Buy tokens and generations$'))
    dp.message.register(Purchase_Handlers.purchase_handler, States.PURCHASE_CHATGPT_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(Purchase_Handlers.purchase_handler,States.PURCHASE_DALL_E_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(Purchase_Handlers.purchase_handler, States.PURCHASE_STABLE_STATE, F.text.regexp(r'^🔙Back$'))

    currencies = ['USDT', 'TON', 'BTC', 'ETH']
    for currency in currencies:
        dp.message.register(Purchase_Handlers.buy_handler, States.PURCHASE_CHATGPT_STATE, F.text.regexp(rf'^💲{currency}$'))
        dp.message.register(Purchase_Handlers.buy_handler, States.PURCHASE_DALL_E_STATE, F.text.regexp(rf'^💲{currency}$'))
        dp.message.register(Purchase_Handlers.buy_handler, States.PURCHASE_STABLE_STATE, F.text.regexp(rf'^💲{currency}$'))

    dp.message.register(Purchase_Handlers.currencies_handler, States.PURCHASE_STATE, F.text.regexp(r'^100K ChatGPT tokens - 5 USD💵$'))
    dp.message.register(Purchase_Handlers.currencies_handler, States.PURCHASE_STATE, F.text.regexp(r'^50 DALL·E image generations - 5 USD💵$'))
    dp.message.register(Purchase_Handlers.currencies_handler, States.PURCHASE_STATE, F.text.regexp(r'^50 Stable Diffusion image generations - 5 USD💵$'))

def register_start_handlers(dp: Dispatcher, database: DataBase):
    Start_Handler = StartHandler(database)
    dp.message.register(Start_Handler.start_handler, Command('start'))
    dp.message.register(Start_Handler.start_handler, States.ENTRY_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(Start_Handler.start_handler, States.CHATGPT_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(Start_Handler.start_handler, States.DALL_E_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(Start_Handler.start_handler, States.STABLE_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(Start_Handler.start_handler, States.INFO_STATE, F.text.regexp(r'^🔙Back$'))

def register_question_handlers(dp: Dispatcher):
    dp.message.register(question_handler, States.ENTRY_STATE, F.text.regexp(r'^💭Chatting — ChatGPT-4o$'))
    dp.message.register(question_handler, States.ENTRY_STATE, F.text.regexp(r'^🌄Image generation — DALL·E 3$'))
    dp.message.register(question_handler, States.ENTRY_STATE, F.text.regexp(r'^🌅Image generation — Stable Diffusion 3$'))

def register_display_info_handlers(dp: Dispatcher, database: DataBase):
    Display_Info = DisplayInfo(database)
    dp.message.register(Display_Info.display_info_handler, States.ENTRY_STATE, F.text.regexp(r'^👤My account | 💰Buy$'))
    dp.message.register(Display_Info.display_info_handler, States.PURCHASE_STATE, F.text.regexp(r'^🔙Back$'))


def register_answer_handlers(dp: Dispatcher, database: DataBase, openai: OpenAiTools, stable: StableDiffusion):
    Answer_Handlers = AnswerHandlers(database, openai, stable)
    dp.message.register(Answer_Handlers.chatgpt_answer_handler, States.CHATGPT_STATE, F.text)
    dp.message.register(Answer_Handlers.stable_answer_handler, States.STABLE_STATE, F.text)
    dp.message.register(Answer_Handlers.dall_e_answer_handler, States.DALL_E_STATE, F.text)