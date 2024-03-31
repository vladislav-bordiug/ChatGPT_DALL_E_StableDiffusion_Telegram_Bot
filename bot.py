from gpytranslate import Translator

from os import getenv
from tiktoken import encoding_for_model

from db import DataBase
from openaitools import OpenAiTools
from stablediffusion import StableDiffusion
from cryptopay import CryptoPay

from dotenv import load_dotenv
from aiofiles.os import remove

import asyncio

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram import F

load_dotenv()
translator = Translator()
encoding = encoding_for_model("gpt-3.5-turbo")
bot = Bot(token=getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(bot)

class States(StatesGroup):
    ENTRY_STATE = State()
    CHATGPT_STATE = State()
    DALL_E_STATE = State()
    STABLE_STATE = State()
    INFO_STATE = State()
    PURCHASE_CHATGPT_STATE = State()
    PURCHASE_DALL_E_STATE = State()
    PURCHASE_STABLE_STATE = State()

# Starts a conversation
@dp.message_handler(Command('start'))
@dp.message_handler(F.text=='🔙Back', state=[States.ENTRY_STATE, States.CHATGPT_STATE, States.DALL_E_STATE, States.STABLE_STATE, States.INFO_STATE])
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    result = await DataBase.is_user(user_id)

    button = [[KeyboardButton(text="💭Chatting — ChatGPT")],
              [KeyboardButton(text="🌄Image generation — DALL·E")],
              [KeyboardButton(text="🌅Image generation — Stable Diffusion")],
              [KeyboardButton(text="👤My account | 💰Buy")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    if not result:
        await DataBase.insert_user(user_id, username)
        await message.reply_text(
            text = "👋You have: \n💭3000 ChatGPT tokens \n🌄3 DALL·E Image Generations \n🌅3 Stable Diffusion Image generations\n Choose an option: 👇 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )
    else:
        await message.reply_text(
            text = "Choose an option: 👇🏻 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )
    await States.ENTRY_STATE.set()

# Question Handling
@dp.message_handler(F.text=='💭Chatting — ChatGPT$', state=States.ENTRY_STATE)
@dp.message_handler(F.text=='🌄Image generation — DALL·E$', state=States.ENTRY_STATE)
@dp.message_handler(F.text=='🌅Image generation — Stable Diffusion$', state=States.ENTRY_STATE)
async def question_handler(message: types.Message):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await message.reply_text(
        text = "Enter your text: 👇🏻",
        reply_markup=reply_markup,
    )
    option = message.text
    if option == "💭Chatting — ChatGPT":
        await States.CHATGPT_STATE.set()
    elif option == "🌄Image generation — DALL·E":
        await States.DALL_E_STATE.set()
    elif option == "🌅Image generation — Stable Diffusion":
        await States.STABLE_STATE.set()

# Answer Handling
@dp.message_handler(F.text, state=States.CHATGPT_STATE)
async def chatgpt_answer_handler(message: types.Message):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    user_id = message.from_user.id
    result = await DataBase.get_chatgpt(user_id)

    if result > 0:
        question = message.text

        answer = await OpenAiTools.get_chatgpt(question)

        if answer:
            await message.reply_text(
                text = answer,
                reply_markup=reply_markup,
            )
            result -= len(await asyncio.get_running_loop().run_in_executor(None, encoding.encode,question)) + len(await asyncio.get_running_loop().run_in_executor(None, encoding.encode,answer))
            if result > 0:
                await DataBase.set_chatgpt(user_id, result)
            else:
                await DataBase.set_chatgpt(user_id, 0)
        else:
            await message.reply_text(
                text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )

    else:
        await message.reply_text(
            text = "❎You have 0 ChatGPT tokens. You need to buy them to use ChatGPT.",
            reply_markup=reply_markup,
        )
    await States.CHATGPT_STATE.set()


# Answer Handling
@dp.message_handler(F.text, state=States.DALL_E_STATE)
async def dall_e_answer_handler(message: types.Message):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    user_id = message.from_user.id
    result = await DataBase.get_dalle(user_id)

    if result > 0:
        question = message.text

        prompt = await translator.translate(question, targetlang='en')

        answer = await OpenAiTools.get_dalle(prompt.text)

        if answer:
            await message.reply_photo(
                photo=answer,
                reply_markup=reply_markup,
                caption=question,
            )
            result -= 1
            await DataBase.set_dalle(user_id, result)
        else:
            await message.reply_text(
                text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )
    else:
        await message.reply_text(
            text = "❎You have 0 DALL·E image generations. You need to buy them to use DALL·E.",
            reply_markup=reply_markup,
        )
    await States.DALL_E_STATE.set()


# Answer Handling
@dp.message_handler(F.text, state=States.STABLE_STATE)
async def stable_answer_handler(message: types.Message):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    user_id = message.from_user.id
    result = await DataBase.get_stable(user_id)

    if result > 0:

        question = message.text

        prompt = await translator.translate(question, targetlang='en')

        path = await asyncio.get_running_loop().run_in_executor(None, StableDiffusion.get_stable,prompt.text)

        if path:
            await message.reply_photo(
                photo=open(path, 'rb'),
                reply_markup=reply_markup,
                caption=question,
            )
            await remove(path)
            result -= 1
            await DataBase.set_stable(user_id, result)
        else:
            await message.reply_text(
                text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )
    else:
        await message.reply_text(
            text = "❎You have 0 Stable Diffusion image generations. You need to buy them to use Stable Diffusion.",
            reply_markup=reply_markup,
        )
    await States.STABLE_STATE.set()


# Displays information about user
@dp.message_handler(F.text=='👤My account | 💰Buy$', state=States.ENTRY_STATE)
@dp.message_handler(F.text=='🔙Back', state=States.PURCHASE_STATE)
async def display_info(message: types.Message):
    user_id = message.from_user.id
    result = await DataBase.get_userinfo(user_id)

    button = [[KeyboardButton(text="💰Buy tokens and generations")], [KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await message.reply_text(
        text = f"You have: \n 💭{result[2]} ChatGPT tokens \n 🌄{result[3]} DALL·E image generations \n 🌅{result[4]} Stable Diffusion image generations \n 💸 You can buy more with crypto",
        reply_markup=reply_markup,
    )
    await States.INFO_STATE.set()


# Displays goods
@dp.message_handler(F.text=='💰Buy tokens and generations$', state=States.INFO_STATE)
@dp.message_handler(F.text=='🔙Back', state=[States.PURCHASE_CHATGPT_STATE,States.PURCHASE_DALL_E_STATE,States.PURCHASE_STABLE_STATE])
async def purchase(message: types.Message):
    button = [[KeyboardButton(text="100K ChatGPT tokens - 5 USD💵")],
              [KeyboardButton(text="100 DALL·E image generations - 5 USD💵")],
              [KeyboardButton(text="100 Stable Diffusion image generations - 5 USD💵")], [KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await message.reply_text(
        text = "Choose product: 👇",
        reply_markup=reply_markup,
    )
    await States.PURCHASE_STATE.set()


# Displays cryptocurrencies
@dp.message_handler(F.text=='100K ChatGPT tokens - 5 USD💵$', state=States.PURCHASE_STATE)
@dp.message_handler(F.text=='100 DALL·E image generations - 5 USD💵$', state=States.PURCHASE_STATE)
@dp.message_handler(F.text=='100 Stable Diffusion image generations - 5 USD💵$', state=States.PURCHASE_STATE)
async def currencies(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="💲USDT"),
             KeyboardButton(text="💲TON")],
            [KeyboardButton(text="💲BTC"),
             KeyboardButton(text="💲ETH")],
            [KeyboardButton(text="🔙Back")]
        ],
        resize_keyboard=True
    )
    await message.reply_text(
        text = "Choose currency: 👇",
        reply_markup=keyboard,
    )
    product = message.text
    if product == "100K ChatGPT tokens - 5 USD💵":
        await States.PURCHASE_CHATGPT_STATE.set()
    elif product == "100 DALL·E image generations - 5 USD💵":
        await States.PURCHASE_DALL_E_STATE.set()
    elif product == "100 Stable Diffusion image generations - 5 USD💵":
        await States.PURCHASE_STABLE_STATE.set()

# Makes invoice and displays it
@dp.message_handler(F.text=='💲USDT$', state=States.PURCHASE_CHATGPT_STATE)
@dp.message_handler(F.text=='💲TON$', state=States.PURCHASE_CHATGPT_STATE)
@dp.message_handler(F.text=='💲BTC$', state=States.PURCHASE_CHATGPT_STATE)
@dp.message_handler(F.text=='💲ETH$', state=States.PURCHASE_CHATGPT_STATE)
async def buy_chatgpt(message: types.Message):
    user_id = message.from_user.id
    currency = message.text
    invoice_url, invoice_id = await CryptoPay.create_invoice(5, currency[1:])
    await DataBase.new_order(invoice_id, user_id, 'chatgpt')
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💰Buy", url=invoice_url),
             InlineKeyboardButton(text="☑️Check", callback_data=str(invoice_id))],
        ]
    )
    await message.reply_text(
        text = "💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗️Consider the network commission \n ☑️After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
    )


# Makes invoice and displays it
@dp.message_handler(F.text=='💲USDT$', state=States.PURCHASE_DALL_E_STATE)
@dp.message_handler(F.text=='💲TON$', state=States.PURCHASE_DALL_E_STATE)
@dp.message_handler(F.text=='💲BTC$', state=States.PURCHASE_DALL_E_STATE)
@dp.message_handler(F.text=='💲ETH$', state=States.PURCHASE_DALL_E_STATE)
async def buy_dall_e(message: types.Message):
    user_id = message.from_user.id
    currency = message.text
    invoice_url, invoice_id = await CryptoPay.create_invoice(5, currency[1:])
    await DataBase.new_order(invoice_id, user_id, 'dall_e')
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💰Buy", url=invoice_url),
             InlineKeyboardButton(text="☑️Check", callback_data=str(invoice_id))],
        ]
    )
    await message.reply_text(
        text = "💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗️Consider the network commission \n ☑️After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
    )


# Makes invoice and displays it
@dp.message_handler(F.text=='💲USDT$', state=States.PURCHASE_STABLE_STATE)
@dp.message_handler(F.text=='💲TON$', state=States.PURCHASE_STABLE_STATE)
@dp.message_handler(F.text=='💲BTC$', state=States.PURCHASE_STABLE_STATE)
@dp.message_handler(F.text=='💲ETH$', state=States.PURCHASE_STABLE_STATE)
async def buy_stable(message: types.Message):
    user_id = message.from_user.id
    currency = message.text
    invoice_url, invoice_id = await CryptoPay.create_invoice(5, currency[1:])
    await DataBase.new_order(invoice_id, user_id, 'stable')
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💰Buy", url=invoice_url),
             InlineKeyboardButton(text="☑️Check", callback_data=str(invoice_id))],
        ]
    )
    await message.reply_text(
        text = "💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗️Consider the network commission \n ☑️After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
    )


# Checks payment
@dp.callback_query_handler()
async def keyboard_callback(callback_query: types.CallbackQuery):
    query = callback_query
    invoice_id = int(query.data)
    result = await DataBase.get_orderdata(invoice_id)
    if result:
        status = await CryptoPay.get_status(invoice_id)
        if status == "active":
            await query.answer("⌚️We have not received payment yet")
        elif status == "paid":
            if result[1] == 'chatgpt':
                await DataBase.update_chatgpt(result[0], invoice_id)
                await query.answer("✅Successful payment, tokens were added to your account")
            elif result[1] == 'dall_e':
                await DataBase.update_dalle(result[0], invoice_id)
                await query.answer("✅Successful payment, image generations were added to your account")
            elif result[1] == 'stable':
                await DataBase.update_stable(result[0], invoice_id)
                await query.answer("✅Successful payment, image generations were added to your account")
        elif status == "expired":
            await query.answer("❎Payment has expired, create a new payment")
    else:
        await query.answer("❎Payment has expired, create a new payment")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)