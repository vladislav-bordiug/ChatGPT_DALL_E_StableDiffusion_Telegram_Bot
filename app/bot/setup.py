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

def register_handlers(dp: Dispatcher):
    register_purchase_handlers(dp)

    register_start_handlers(dp)

    register_question_handlers(dp)

    register_display_info_handlers(dp)

    register_answer_handlers(dp)

def register_purchase_handlers(dp: Dispatcher):
    dp.message.register(purchase_handler, States.INFO_STATE, F.text.regexp(r'^💰Buy tokens and generations$'))
    dp.message.register(purchase_handler, States.PURCHASE_CHATGPT_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(purchase_handler,States.PURCHASE_DALL_E_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(purchase_handler, States.PURCHASE_STABLE_STATE, F.text.regexp(r'^🔙Back$'))

    currencies = ['USDT', 'TON', 'BTC', 'ETH']
    for currency in currencies:
        dp.message.register(buy_handler, States.PURCHASE_CHATGPT_STATE, F.text.regexp(rf'^💲{currency}$'))
        dp.message.register(buy_handler, States.PURCHASE_DALL_E_STATE, F.text.regexp(rf'^💲{currency}$'))
        dp.message.register(buy_handler, States.PURCHASE_STABLE_STATE, F.text.regexp(rf'^💲{currency}$'))

def register_start_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command('start'))
    dp.message.register(start_handler, States.ENTRY_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(start_handler, States.CHATGPT_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(start_handler, States.DALL_E_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(start_handler, States.STABLE_STATE, F.text.regexp(r'^🔙Back$'))
    dp.message.register(start_handler, States.INFO_STATE, F.text.regexp(r'^🔙Back$'))

def register_question_handlers(dp: Dispatcher):
    dp.message.register(question_handler, States.ENTRY_STATE, F.text.regexp(r'^💭Chatting — ChatGPT-4o$'))
    dp.message.register(question_handler, States.ENTRY_STATE, F.text.regexp(r'^🌄Image generation — DALL·E 3$'))
    dp.message.register(question_handler, States.ENTRY_STATE, F.text.regexp(r'^🌅Image generation — Stable Diffusion 3$'))

def register_display_info_handlers(dp: Dispatcher):
    dp.message.register(display_info_handler, States.ENTRY_STATE, F.text.regexp(r'^👤My account | 💰Buy$'))
    dp.message.register(display_info_handler, States.PURCHASE_STATE, F.text.regexp(r'^🔙Back$'))

def register_answer_handlers(dp: Dispatcher):
    dp.message.register(chatgpt_answer_handler, States.CHATGPT_STATE, F.text)
    dp.message.register(stable_answer_handler, States.STABLE_STATE, F.text)
    dp.message.register(dall_e_answer_handler, States.DALL_E_STATE, F.text)
    dp.message.register(currencies_handler, States.PURCHASE_STATE, F.text.regexp(r'^100K ChatGPT tokens - 5 USD💵$'))
    dp.message.register(currencies_handler, States.PURCHASE_STATE, F.text.regexp(r'^50 DALL·E image generations - 5 USD💵$'))
    dp.message.register(currencies_handler, States.PURCHASE_STATE, F.text.regexp(r'^50 Stable Diffusion image generations - 5 USD💵$'))