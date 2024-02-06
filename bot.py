from deep_translator import GoogleTranslator

import os

import db
from chatgpt import Chatgpt
from stablediffusion import StableDiffusion
from dalle import DallE
from dotenv import load_dotenv
from aiocryptopay import AioCryptoPay, Networks, utils
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


# Gets answer from chatgpt
def _generate_chatgpt(prompt: str):
    chatgpt = Chatgpt()
    c = chatgpt.get_answer(prompt)
    return c


# Translates text into English
def _translate(text: str):
    translator = GoogleTranslator(source='auto', target='en')
    t = translator.translate(text)
    return t


# Converts text to image using Stable Diffusion
def _stable_diffusion(text: str):
    stablediffusion = StableDiffusion()
    image = stablediffusion.to_image(text)
    return image


# Converts text to image using Dall E
def _dall_e(text: str):
    dalle = DallE()
    image = dalle.to_image(text)
    return image


# Starts a conversation
async def start(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    result = db.is_user(user_id)

    button = [[KeyboardButton(text="💭Chatting — ChatGPT 3.5 Turbo")],
              [KeyboardButton(text="🌄Image generation — DALL·E")],
              [KeyboardButton(text="🌅Image generation — Stable Diffusion")],
              [KeyboardButton(text="👤My account | 💰Buy")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    if not result:
        db.insert_user(user_id, username)
        await update.message.reply_text(
            "👋You have: \n💭3000 ChatGPT tokens \n🌄3 DALL·E Image Generations \n🌅3 Stable Diffusion Image generations\n Choose an option: 👇 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(
            "Choose an option: 👇🏻 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )
    return ENTRY_STATE


# Question Handling
async def pre_chatgpt_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        "Enter your text: 👇🏻",
        reply_markup=reply_markup,
    )
    return CHATGPT_STATE


# Question Handling
async def pre_stable_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        "Enter your text: 👇🏻",
        reply_markup=reply_markup,
    )
    return STABLE_STATE


# Question Handling
async def pre_dall_e_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        "Enter your text: 👇🏻",
        reply_markup=reply_markup,
    )
    return DALL_E_STATE


# Answer Handling
async def pre_chatgpt_answer_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    user_id = update.message.from_user.id
    result = db.get_chatgpt(user_id)

    if result > 0:
        question = update.message.text

        answer = _generate_chatgpt(question)

        if answer != None:
            await update.message.reply_text(
                answer,
                reply_markup=reply_markup,
            )
            result -= len(question) + len(answer)
            if result > 0:
                db.set_chatgpt(user_id, result)
            else:
                db.set_chatgpt(user_id, 0)
        else:
            await update.message.reply_text(
                "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )

    else:
        await update.message.reply_text(
            "❎You have 0 ChatGPT tokens. You need to buy them to use ChatGPT.",
            reply_markup=reply_markup,
        )
    return CHATGPT_STATE


# Answer Handling
async def pre_dall_e_answer_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    user_id = update.message.from_user.id
    result = db.get_dalle(user_id)

    if result > 0:
        question = update.message.text

        prompt = _translate(question)

        answer = _dall_e(prompt)

        if answer:
            await update.message.reply_photo(
                photo=answer,
                reply_markup=reply_markup,
                caption=question,
            )
            result -= 1
            db.set_dalle(user_id, result)
        else:
            await update.message.reply_text(
                "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )
    else:
        await update.message.reply_text(
            "❎You have 0 DALL·E image generations. You need to buy them to use DALL·E.",
            reply_markup=reply_markup,
        )
    return DALL_E_STATE


# Answer Handling
async def pre_stable_answer_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    user_id = update.message.from_user.id
    result = db.get_stable(user_id)

    if result > 0:
        question = update.message.text

        prompt = _translate(question)

        path = _stable_diffusion(prompt)

        try:
            await update.message.reply_photo(
                photo=open(path, 'rb'),
                reply_markup=reply_markup,
                caption=question,
            )
            os.remove(path)
        except:
            await update.message.reply_text(
                "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
                reply_markup=reply_markup,
            )
        else:
            result -= 1
            db.set_stable(user_id, result)
    else:
        await update.message.reply_text(
            "❎You have 0 Stable Diffusion image generations. You need to buy them to use Stable Diffusion.",
            reply_markup=reply_markup,
        )
    return STABLE_STATE


# Displays information about user
async def display_info(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    result = db.get_userinfo(user_id)

    button = [[KeyboardButton(text="💰Buy tokens and generations")], [KeyboardButton(text="🔙Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        f"You have: \n 💭{result[2]} ChatGPT tokens \n 🌄{result[3]} DALL·E image generations \n 🌅{result[4]} Stable Diffusion image generations \n 💸 You can buy more with crypto",
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
        "Choose product: 👇",
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
        "Choose currency: 👇",
        reply_markup=keyboard,
    )
    product = update.message.text
    if product == "100K ChatGPT tokens - 5 USD💵":
        return PURCHASE_CHATGPT_STATE
    elif product == "100 DALL·E image generations - 5 USD💵":
        return PURCHASE_DALL_E_STATE
    elif product == "100 Stable Diffusion image generations - 5 USD💵":
        return PURCHASE_STABLE_STATE


# Get price
async def getprice(cost, currency):
    rates = await crypto.get_exchange_rates()
    if currency == "💲USDT":
        exchange = float((utils.exchange.get_rate('USDT', 'USD', rates)).rate)
        price = cost / exchange
    elif currency == "💲TON":
        exchange = float((utils.exchange.get_rate('TON', 'USD', rates)).rate)
        price = cost / exchange
    elif currency == "💲BTC":
        exchange = float((utils.exchange.get_rate('BTC', 'USD', rates)).rate)
        price = cost / exchange
    elif currency == "💲ETH":
        exchange = float((utils.exchange.get_rate('ETH', 'USD', rates)).rate)
        price = cost / exchange
    return price


# Makes invoice and displays it
async def buy_chatgpt(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    currency = update.message.text
    price = getprice(5, currency)
    invoice = await crypto.create_invoice(asset=currency[1:], amount=price)
    db.new_order(invoice.invoice_id, user_id, 'chatgpt')
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💰Buy", url=invoice.bot_invoice_url),
             InlineKeyboardButton(text="☑️Check", callback_data=invoice.invoice_id)],
        ]
    )
    await update.message.reply_text(
        "💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗️Consider the network commission \n ☑️After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
    )


# Makes invoice and displays it
async def buy_dall_e(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    currency = update.message.text
    price = getprice(5, currency)
    invoice = await crypto.create_invoice(asset=currency[1:], amount=price)
    db.new_order(invoice.invoice_id, user_id, 'dall_e')
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💰Buy", url=invoice.bot_invoice_url),
             InlineKeyboardButton(text="☑️Check", callback_data=invoice.invoice_id)],
        ]
    )
    await update.message.reply_text(
        "💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗️Consider the network commission \n ☑️After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
    )


# Makes invoice and displays it
async def buy_stable(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    currency = update.message.text
    price = getprice(5, currency)
    invoice = await crypto.create_invoice(asset=currency[1:], amount=price)
    db.new_order(invoice.invoice_id, user_id, 'stable')
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💰Buy", url=invoice.bot_invoice_url),
             InlineKeyboardButton(text="☑️Check", callback_data=invoice.invoice_id)],
        ]
    )
    await update.message.reply_text(
        "💳If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n ❗️Consider the network commission \n ☑️After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
    )


# Checks payment
async def keyboard_callback(update: Update, context: ContextTypes):
    query = update.callback_query
    invoice_id = query.data
    result = db.get_orderdata(invoice_id)
    if result:
        invoices = await crypto.get_invoices(invoice_ids=invoice_id)
        if invoices.status == "active":
            await query.answer("⌚️We have not received payment yet")
        elif invoices.status == "paid":
            if result[1] == 'chatgpt':
                db.update_chatgpt(result[0], invoice_id)
                await query.answer("✅Successful payment, tokens were added to your account")
            elif result[1] == 'dall_e':
                db.update_dalle(result[0], invoice_id)
                await query.answer("✅Successful payment, image generations were added to your account")
            elif result[1] == 'stable':
                db.update_stable(result[0], invoice_id)
                await query.answer("✅Successful payment, image generations were added to your account")
        elif invoices.status == "expired":
            await query.answer("❎Payment has expired, create a new payment")
    else:
        await query.answer("❎Payment has expired, create a new payment")


if __name__ == '__main__':
    load_dotenv()
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).read_timeout(100).get_updates_read_timeout(100).build()
    crypto = AioCryptoPay(token=os.getenv("CRYPTOPAY_KEY"), network=Networks.MAIN_NET)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), MessageHandler(filters.Regex('^🔙Back$'), start)],
        states={
            ENTRY_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^💭Chatting — ChatGPT 3.5 Turbo$'), pre_chatgpt_handler),
                MessageHandler(filters.Regex('^🌄Image generation — DALL·E$'), pre_dall_e_handler),
                MessageHandler(filters.Regex('^🌅Image generation — Stable Diffusion$'), pre_stable_handler),
                MessageHandler(filters.Regex('^👤My account | 💰Buy$'), display_info),
                MessageHandler(filters.Regex('^🔙Back$'), start),
            ],
            CHATGPT_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), start),
                MessageHandler(filters.TEXT, pre_chatgpt_answer_handler),
            ],
            DALL_E_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), start),
                MessageHandler(filters.TEXT, pre_dall_e_answer_handler),
            ],
            STABLE_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^🔙Back$'), start),
                MessageHandler(filters.TEXT, pre_stable_answer_handler),
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