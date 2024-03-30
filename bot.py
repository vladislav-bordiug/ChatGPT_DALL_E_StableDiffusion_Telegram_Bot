from deep_translator import GoogleTranslator

from os import getenv
from tiktoken import encoding_for_model

from db import DataBase
from openaitools import OpenAiTools
from stablediffusion import StableDiffusion
from cryptopay import CryptoPay

from dotenv import load_dotenv
from aiofiles.os import remove

from asyncio import get_running_loop
from contextvars import copy_context
from functools import partial

async def to_thread(func, /, *args, **kwargs):
    loop = get_running_loop()
    ctx = copy_context()
    func_call = partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    Message,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

(ENTRY_STATE, CHATGPT_STATE,
 DALL_E_STATE, STABLE_STATE,
 INFO_STATE, PURCHASE_STATE,
 PURCHASE_CHATGPT_STATE,
 PURCHASE_DALL_E_STATE, PURCHASE_STABLE_STATE) = range(9)

# Starts a conversation
async def start(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    result = await to_thread(DataBase.is_user,user_id)

    button = [[KeyboardButton(text="💭Chatting — ChatGPT")],
              [KeyboardButton(text="🌄Image generation — DALL·E")],
              [KeyboardButton(text="🌅Image generation — Stable Diffusion")],
              [KeyboardButton(text="👤My account | 💰Buy")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    if not result:
        await to_thread(DataBase.insert_user,user_id, username)
        await update.message.reply_text(
            text = "👋You have: \n💭3000 ChatGPT tokens \n🌄3 DALL·E Image Generations \n🌅3 Stable Diffusion Image generations\n Choose an option: 👇 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(
            text = "Choose an option: 👇🏻 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )
    return ENTRY_STATE

# Question Handling
async def question_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        text = "Enter your text: 👇🏻",
        reply_markup=reply_markup,
    )
    option = update.message.text
    if option == "💭Chatting — ChatGPT":
        return CHATGPT_STATE
    elif option == "🌄Image generation — DALL·E":
        return DALL_E_STATE
    elif option == "🌅Image generation — Stable Diffusion":
        return STABLE_STATE

# Answer Handling
async def chatgpt_answer_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    user_id = update.message.from_user.id
    result = await to_thread(DataBase.get_chatgpt,user_id)

    if result > 0:
        question = update.message.text

        answer = await to_thread(OpenAiTools.get_chatgpt,question)

        if answer:
            await update.message.reply_text(
                text = answer,
                reply_markup=reply_markup,
            )
            result -= len(await to_thread(encoding.encode,question)) + len(await to_thread(encoding.encode,answer))
            if result > 0:
                await to_thread(DataBase.set_chatgpt,user_id, result)
            else:
                await to_thread(DataBase.set_chatgpt,user_id, 0)
        else:
            await update.message.reply_text(
                text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )

    else:
        await update.message.reply_text(
            text = "❎You have 0 ChatGPT tokens. You need to buy them to use ChatGPT.",
            reply_markup=reply_markup,
        )
    return CHATGPT_STATE


# Answer Handling
async def dall_e_answer_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    user_id = update.message.from_user.id
    result = await to_thread(DataBase.get_dalle,user_id)

    if result > 0:
        question = update.message.text

        prompt = await to_thread(translator.translate,question)

        answer = await to_thread(OpenAiTools.get_dalle,prompt)

        if answer:
            await update.message.reply_photo(
                photo=answer,
                reply_markup=reply_markup,
                caption=question,
            )
            result -= 1
            await to_thread(DataBase.set_dalle,user_id, result)
        else:
            await update.message.reply_text(
                text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )
    else:
        await update.message.reply_text(
            text = "❎You have 0 DALL·E image generations. You need to buy them to use DALL·E.",
            reply_markup=reply_markup,
        )
    return DALL_E_STATE


# Answer Handling
async def stable_answer_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    user_id = update.message.from_user.id
    result = await to_thread(DataBase.get_stable,user_id)

    if result > 0:

        question = update.message.text

        prompt = await to_thread(translator.translate,question)

        path = await to_thread(StableDiffusion.get_stable,prompt)

        if path:
            await update.message.reply_photo(
                photo=open(path, 'rb'),
                reply_markup=reply_markup,
                caption=question,
            )
            await remove(path)
            result -= 1
            await to_thread(DataBase.set_stable,user_id, result)
        else:
            await update.message.reply_text(
                text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )
    else:
        await update.message.reply_text(
            text = "❎You have 0 Stable Diffusion image generations. You need to buy them to use Stable Diffusion.",
            reply_markup=reply_markup,
        )
    return STABLE_STATE


# Displays information about user
async def display_info(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    result = await to_thread(DataBase.get_userinfo,user_id)

    button = [[KeyboardButton(text="💰Buy tokens and generations")], [KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        text = f"You have: \n 💭{result[2]} ChatGPT tokens \n 🌄{result[3]} DALL·E image generations \n 🌅{result[4]} Stable Diffusion image generations \n 💸 You can buy more with crypto",
        reply_markup=reply_markup,
    )
    return INFO_STATE


# Displays goods
async def purchase(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="100K ChatGPT tokens - 5 USD💵")],
              [KeyboardButton(text="100 DALL·E image generations - 5 USD💵")],
              [KeyboardButton(text="100 Stable Diffusion image generations - 5 USD💵")], [KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        text = "Choose product: 👇",
        reply_markup=reply_markup,
    )
    return PURCHASE_STATE


# Displays cryptocurrencies
async def currencies(update: Update, context: ContextTypes):
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
    await update.message.reply_text(
        text = "Choose currency: 👇",
        reply_markup=keyboard,
    )
    product = update.message.text
    if product == "100K ChatGPT tokens - 5 USD💵":
        return PURCHASE_CHATGPT_STATE
    elif product == "100 DALL·E image generations - 5 USD💵":
        return PURCHASE_DALL_E_STATE
    elif product == "100 Stable Diffusion image generations - 5 USD💵":
        return PURCHASE_STABLE_STATE

# Makes invoice and displays it
async def buy_chatgpt(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    currency = update.message.text
    invoice_url, invoice_id = await CryptoPay.create_invoice(5, currency[1:])
    await to_thread(DataBase.new_order,invoice_id, user_id, 'chatgpt')
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💰Buy", url=invoice_url),
             InlineKeyboardButton(text="☑️Check", callback_data=str(invoice_id))],
        ]
    )
    await update.message.reply_text(
        text = "💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗️Consider the network commission \n ☑️After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
    )


# Makes invoice and displays it
async def buy_dall_e(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    currency = update.message.text
    invoice_url, invoice_id = await CryptoPay.create_invoice(5, currency[1:])
    await to_thread(DataBase.new_order,invoice_id, user_id, 'dall_e')
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💰Buy", url=invoice_url),
             InlineKeyboardButton(text="☑️Check", callback_data=str(invoice_id))],
        ]
    )
    await update.message.reply_text(
        text = "💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗️Consider the network commission \n ☑️After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
    )


# Makes invoice and displays it
async def buy_stable(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    currency = update.message.text
    invoice_url, invoice_id = await CryptoPay.create_invoice(5, currency[1:])
    await to_thread(DataBase.new_order,invoice_id, user_id, 'stable')
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💰Buy", url=invoice_url),
             InlineKeyboardButton(text="☑️Check", callback_data=str(invoice_id))],
        ]
    )
    await update.message.reply_text(
        text = "💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗️Consider the network commission \n ☑️After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
    )


# Checks payment
async def keyboard_callback(update: Update, context: ContextTypes):
    query = update.callback_query
    invoice_id = int(query.data)
    result = await to_thread(DataBase.get_orderdata,invoice_id)
    if result:
        status = await CryptoPay.get_status(invoice_id)
        if status == "active":
            await query.answer("⌚️We have not received payment yet")
        elif status == "paid":
            if result[1] == 'chatgpt':
                await to_thread(DataBase.update_chatgpt,result[0], invoice_id)
                await query.answer("✅Successful payment, tokens were added to your account")
            elif result[1] == 'dall_e':
                await to_thread(DataBase.update_dalle,result[0], invoice_id)
                await query.answer("✅Successful payment, image generations were added to your account")
            elif result[1] == 'stable':
                await to_thread(DataBase.update_stable,result[0], invoice_id)
                await query.answer("✅Successful payment, image generations were added to your account")
        elif status == "expired":
            await query.answer("❎Payment has expired, create a new payment")
    else:
        await query.answer("❎Payment has expired, create a new payment")


if __name__ == '__main__':
    load_dotenv()
    application = Application.builder().token(getenv("TELEGRAM_BOT_TOKEN")).read_timeout(10).get_updates_read_timeout(10).build()
    translator = GoogleTranslator(source='auto', target='en')
    encoding = encoding_for_model("gpt-3.5-turbo")
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), MessageHandler(filters.Regex('^🔙Back$'), start)],
        states={
            ENTRY_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^💭Chatting — ChatGPT$'), question_handler),
                MessageHandler(filters.Regex('^🌄Image generation — DALL·E$'), question_handler),
                MessageHandler(filters.Regex('^🌅Image generation — Stable Diffusion$'), question_handler),
                MessageHandler(filters.Regex('^👤My account | 💰Buy$'), display_info),
                MessageHandler(filters.Regex('^🔙Back$'), start),
            ],
            CHATGPT_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), start),
                MessageHandler(filters.TEXT, chatgpt_answer_handler),
            ],
            DALL_E_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), start),
                MessageHandler(filters.TEXT, dall_e_answer_handler),
            ],
            STABLE_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), start),
                MessageHandler(filters.TEXT, stable_answer_handler),
            ],
            INFO_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), start),
                MessageHandler(filters.Regex('^💰Buy tokens and generations$'), purchase),
            ],
            PURCHASE_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), display_info),
                MessageHandler(filters.Regex('^100K ChatGPT tokens - 5 USD💵$'), currencies),
                MessageHandler(filters.Regex('^100 DALL·E image generations - 5 USD💵$'), currencies),
                MessageHandler(filters.Regex('^100 Stable Diffusion image generations - 5 USD💵$'), currencies),
            ],
            PURCHASE_CHATGPT_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), purchase),
                MessageHandler(filters.Regex('^💲USDT$'), buy_chatgpt),
                MessageHandler(filters.Regex('^💲TON$'), buy_chatgpt),
                MessageHandler(filters.Regex('^💲BTC$'), buy_chatgpt),
                MessageHandler(filters.Regex('^💲ETH$'), buy_chatgpt),
            ],
            PURCHASE_DALL_E_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), purchase),
                MessageHandler(filters.Regex('^💲USDT$'), buy_dall_e),
                MessageHandler(filters.Regex('^💲TON$'), buy_dall_e),
                MessageHandler(filters.Regex('^💲BTC$'), buy_dall_e),
                MessageHandler(filters.Regex('^💲ETH$'), buy_dall_e),
            ],
            PURCHASE_STABLE_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), purchase),
                MessageHandler(filters.Regex('^💲USDT$'), buy_stable),
                MessageHandler(filters.Regex('^💲TON$'), buy_stable),
                MessageHandler(filters.Regex('^💲BTC$'), buy_stable),
                MessageHandler(filters.Regex('^💲ETH$'), buy_stable),
            ],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(keyboard_callback))
    application.run_polling()