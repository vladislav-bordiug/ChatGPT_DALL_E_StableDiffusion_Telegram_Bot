import requests
import deep_translator
from deep_translator import GoogleTranslator
  
import os

import psycopg2
from copilot import Copilot
from text_to_image import TextToImage
from text_to_img import TextToImg
from dotenv import load_dotenv

from aiocryptopay import AioCryptoPay, Networks

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

(ENTRY_STATE, 
QUESTION_STATE,
IMAGE_STATE, DALL_E_STATE, INFO_STATE, PURCHASE_STATE, PURCHASE_CHATGPT_STATE, PURCHASE_DALL_E_STATE, PURCHASE_STABLE_STATE) = range(9)

def _generate_copilot(prompt: str):
    """Gets answer from copilot"""
    
    copilot = Copilot()
    c = copilot.get_answer(prompt)

    return c

def _translate(text: str):
    """Translates the text to English"""
    translator = GoogleTranslator(source='auto', target='en')
    t = translator.translate(text)

    return t

def _to_image(text: str):
    """Converts text to image"""
    
    tti = TextToImage()
    i = tti.to_image(text)

    return i
  
def _dall_e(text: str):
    """Converts text to image"""
    
    tti = TextToImg()
    i = tti.to_image(text)

    return i
  
async def start(update: Update, context: ContextTypes):
    """Start the conversation and ask user for an option."""
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    db_object.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    result = db_object.fetchone()
        
    button = [[KeyboardButton(text="Question-Answering — ChatGPT 3.5 Turbo")], [KeyboardButton(text="Image generation — DALL·E")], [KeyboardButton(text="Image generation — Stable Diffusion")],[KeyboardButton(text="My account | Buy")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    
    if not result:
        db_object.execute("INSERT INTO users(user_id, username, chatgpt, dall_e, stable_diffusion) VALUES (%s, %s, %s, %s, %s)", (user_id, username, 3000,3,3))
        db_connection.commit()
        await update.message.reply_text(
            "You have free 3000 ChatGPT tokens, 3 DALL·E Image Generations and 3 Stable Diffusion Image generations\n Choose an option: 👇 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(
            "Choose an option: 👇🏻 \n If buttons don't work, enter /start command",
            reply_markup=reply_markup,
        )

    return ENTRY_STATE

#Handling the question
async def pre_query_handler(update: Update, context: ContextTypes):
    """Ask the user for a query."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Enter your text: 👇🏻",
        reply_markup=reply_markup,
    )

    return QUESTION_STATE

#Handling the question
async def pre_image_handler(update: Update, context: ContextTypes):
    """Ask the user for a query."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Enter your text: 👇🏻",
        reply_markup=reply_markup,
    )

    return IMAGE_STATE
  
async def pre_dall_e(update: Update, context: ContextTypes):
    """Ask the user for a query."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Enter your text: 👇🏻",
        reply_markup=reply_markup,
    )

    return DALL_E_STATE
  
#Handling the answer
async def pre_query_answer_handler(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    
    user_id = update.message.from_user.id
    db_object.execute(f"SELECT chatgpt FROM users WHERE user_id = {user_id}")
    result = int(db_object.fetchone()[0])
    
    if result > 0:
        question = update.message.text

        answer = _generate_copilot(question)

        context.user_data['answer'] = answer

        if answer != None:
            await update.message.reply_text(
                answer, 
                reply_markup=reply_markup,
            )
            result -= len(question) + len(answer)
            if result > 0:
                db_object.execute(f"UPDATE users SET chatgpt = {result} WHERE user_id = {user_id}")
                db_connection.commit()
            else:
                db_object.execute(f"UPDATE users SET chatgpt = 0 WHERE user_id = {user_id}")
                db_connection.commit()
        else:
            await update.message.reply_text(
                "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.", 
                reply_markup=reply_markup,
            )
        
    else:
        await update.message.reply_text(
            "Your have 0 ChatGPT tokens. You need to buy them to use ChatGPT.", 
            reply_markup=reply_markup,
            )

    return QUESTION_STATE

async def pre_image_answer_handler(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    
    user_id = update.message.from_user.id
    db_object.execute(f"SELECT stable_diffusion FROM users WHERE user_id = {user_id}")
    result = int(db_object.fetchone()[0])
    
    if result > 0:
        question = update.message.text

        en_v = _translate(question)

        path = _to_image(en_v)
        context.user_data['image_path'] = _to_image

        try:
            await update.message.reply_photo(
                photo=open(path, 'rb'), 
                reply_markup=reply_markup, 
                caption=question, 
                )
            os.remove(path)
        except:
            await update.message.reply_text(
                "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.", 
                reply_markup=reply_markup,
                )
        else:
            result -= 1
            db_object.execute(f"UPDATE users SET stable_diffusion = {result} WHERE user_id = {user_id}")
            db_connection.commit()
    else:
        await update.message.reply_text(
            "Your have 0 Stable Diffusion image generations. You need to buy them to use Stable Diffusion.", 
            reply_markup=reply_markup,
            )

    return IMAGE_STATE
  
async def pre_dall_e_answer_handler(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    
    user_id = update.message.from_user.id
    db_object.execute(f"SELECT dall_e FROM users WHERE user_id = {user_id}")
    result = int(db_object.fetchone()[0])
    
    if result > 0:
        question = update.message.text

        en_v = _translate(question)

        answer = _dall_e(en_v)
        context.user_data['answer'] = answer

        if answer != None:
            await update.message.reply_photo(
                  photo=answer, 
                  reply_markup=reply_markup, 
                  caption=question, 
                  )
            result -= 1
            db_object.execute(f"UPDATE users SET dall_e = {result} WHERE user_id = {user_id}")
            db_connection.commit()
        else:
            await update.message.reply_text(
              "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.", 
              reply_markup=reply_markup,
              )
    else:
        await update.message.reply_text(
            "Your have 0 DALL·E image generations. You need to buy them to use DALL·E.", 
            reply_markup=reply_markup,
            )

    return DALL_E_STATE
 
async def display_info(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    db_object.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    result = db_object.fetchone()
        
    button = [[KeyboardButton(text="Buy tokens and generations")],[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        f"You have: \n {result[2]} ChatGPT tokens \n {result[3]} DALL·E image generations \n {result[4]} Stable Diffusion image generations",
        reply_markup=reply_markup,
        )

    return INFO_STATE

async def purchase(update: Update, context: ContextTypes):
        
    button = [[KeyboardButton(text="1 million ChatGPT tokens - 5 USDT")],[KeyboardButton(text="100 DALL·E image generations - 5 USDT")],[KeyboardButton(text="100 Stable Diffusion image generations - 5 USDT")],[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        "Choose product: 👇",
        reply_markup=reply_markup,
        )

    return PURCHASE_STATE

async def currencies(update: Update, context: ContextTypes):
    keyboard = ReplyKeyboardMarkup(
         [
            [KeyboardButton(text="USDT"),
            KeyboardButton(text="TON")],
            [KeyboardButton(text="BTC"),
            KeyboardButton(text="ETH")],
            [KeyboardButton(text="Back")]
         ],
         resize_keyboard=True
    )
    await update.message.reply_text(
        "Choose currency: 👇",
        reply_markup=keyboard,
        )
    product = update.message.text
    if product == "1 million ChatGPT tokens - 5 USDT":
        return PURCHASE_CHATGPT_STATE
    elif product == "100 DALL·E image generations - 5 USDT":
        return PURCHASE_DALL_E_STATE
    elif product == "100 Stable Diffusion image generations - 5 USDT":
        return PURCHASE_STABLE_STATE
  
async def buy_chatgpt(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    currency = update.message.text
    price = 5
    if currency == "USDT":
        price = 5
    elif currency == "TON":
        price = 2.57
    elif currency == "BTC":
        price = 0.000033
    elif currency == "ETH":
        price = 0.00052
    invoice = await crypto.create_invoice(asset=currency, amount=price)
    db_object.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    result = db_object.fetchone()
    if not result:
        db_object.execute("INSERT INTO orders(user_id, purchase_id) VALUES (%s, %s)", (user_id, invoice.invoice_id))
        db_connection.commit()
    else:
        db_object.execute(f"UPDATE orders SET purchase_id = {invoice.invoice_id} WHERE user_id = {user_id}")
        db_connection.commit()
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Buy",url=invoice.pay_url),
            InlineKeyboardButton(text="Check",callback_data="ChatGPT_tokens "+str(user_id))],
        ]
    )
    await update.message.reply_text(
        "If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
        )
    
async def buy_dall_e(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    currency = update.message.text
    price = 5
    if currency == "USDT":
        price = 5
    elif currency == "TON":
        price = 2.57
    elif currency == "BTC":
        price = 0.000033
    elif currency == "ETH":
        price = 0.00052
    invoice = await crypto.create_invoice(asset=currency, amount=price)
    db_object.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    result = db_object.fetchone()
    if not result:
        db_object.execute("INSERT INTO orders(user_id, purchase_id) VALUES (%s, %s)", (user_id, invoice.invoice_id))
        db_connection.commit()
    else:
        db_object.execute(f"UPDATE orders SET purchase_id = {invoice.invoice_id} WHERE user_id = {user_id}")
        db_connection.commit()
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Buy",url=invoice.pay_url),
            InlineKeyboardButton(text="Check",callback_data="dall_e "+str(user_id))],
        ]
    )
    await update.message.reply_text(
        "If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
        )
    
async def buy_stable(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    currency = update.message.text
    price = 5
    if currency == "USDT":
        price = 5
    elif currency == "TON":
        price = 2.57
    elif currency == "BTC":
        price = 0.000033
    elif currency == "ETH":
        price = 0.00052
    invoice = await crypto.create_invoice(asset=currency, amount=price)
    db_object.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    result = db_object.fetchone()
    if not result:
        db_object.execute("INSERT INTO orders(user_id, purchase_id) VALUES (%s, %s)", (user_id, invoice.invoice_id))
        db_connection.commit()
    else:
        db_object.execute(f"UPDATE orders SET purchase_id = {invoice.invoice_id} WHERE user_id = {user_id}")
        db_connection.commit()
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Buy",url=invoice.pay_url),
            InlineKeyboardButton(text="Check",callback_data="stable_diffusion "+str(user_id))],
        ]
    )
    await update.message.reply_text(
        "If you want to pay click the button 'Buy', click button 'Start' in Crypto Bot and follow the instructions \n After payment you should tap 'Check' button to check payment \n If you don't want to pay tap the 'Back' button: 👇",
        reply_markup=keyboard,
        )
    
async def keyboard_callback(update: Update, context: ContextTypes):
    query = update.callback_query
    message = query.data.split()[0]
    if message == 'ChatGPT_tokens':
        user_id = query.data.split()[1]
        db_object.execute(f"SELECT purchase_id FROM orders WHERE user_id = {user_id}")
        result = int(db_object.fetchone()[0])
        try:
            invoices = await crypto.get_invoices(invoice_ids=result)
            if invoices.status == "active":
                await query.answer("We have not received payment yet")
            elif invoices.status == "paid":
                db_object.execute(f"UPDATE users SET chatgpt = chatgpt + 1000000 WHERE user_id = {user_id}")
                db_object.execute(f"DELETE FROM orders WHERE user_id = {user_id}")
                db_connection.commit()
                await query.answer("Successful payment, tokens were added to your account")
            elif invoices.status == "expired":
                await query.answer("Payment timed out, create a new payment")
        except:
            await query.answer("Payment timed out, create a new payment")
    if message == 'dall_e':
        user_id = query.data.split()[1]
        db_object.execute(f"SELECT purchase_id FROM orders WHERE user_id = {user_id}")
        result = int(db_object.fetchone()[0])
        try:
            invoices = await crypto.get_invoices(invoice_ids=result)
            if invoices.status == "active":
                await query.answer("We have not received payment yet")
            elif invoices.status == "paid":
                db_object.execute(f"UPDATE users SET dall_e = dall_e + 100 WHERE user_id = {user_id}")
                db_object.execute(f"DELETE FROM orders WHERE user_id = {user_id}")
                db_connection.commit()
                await query.answer("Successful payment, image generations were added to your account")
            elif invoices.status == "expired":
                await query.answer("Payment timed out, create a new payment")
        except:
            await query.answer("Payment timed out, create a new payment")
    if message == 'stable_diffusion':
        user_id = query.data.split()[1]
        db_object.execute(f"SELECT purchase_id FROM orders WHERE user_id = {user_id}")
        result = int(db_object.fetchone()[0])
        try:
            invoices = await crypto.get_invoices(invoice_ids=result)
            if invoices.status == "active":
                await query.answer("We have not received payment yet")
            elif invoices.status == "paid":
                db_object.execute(f"UPDATE users SET stable_diffusion = stable_diffusion + 100 WHERE user_id = {user_id}")
                db_object.execute(f"DELETE FROM orders WHERE user_id = {user_id}")
                db_connection.commit()
                await query.answer("Successful payment, image generations were added to your account")
            elif invoices.status == "expired":
                await query.answer("Payment timed out, create a new payment")
        except:
            await query.answer("Payment timed out, create a new payment")
            
if __name__ == '__main__':
    load_dotenv()
    db_connection = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
    db_object = db_connection.cursor()
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).read_timeout(100).get_updates_read_timeout(100).build()
    crypto = AioCryptoPay(token=os.getenv("CRYPTOPAY_KEY"), network=Networks.MAIN_NET)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),MessageHandler(filters.Regex('^Back$'), start)],
        states={
            ENTRY_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Question-Answering — ChatGPT 3.5 Turbo$'), pre_query_handler),
                MessageHandler(filters.Regex('^Image generation — DALL·E$'), pre_dall_e),
                MessageHandler(filters.Regex('^Image generation — Stable Diffusion$'), pre_image_handler),
                MessageHandler(filters.Regex('^My account | Buy$'), display_info),
                MessageHandler(filters.Regex('^Back$'), start),
            ],
            QUESTION_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Back$'), start),
                MessageHandler(filters.TEXT, pre_query_answer_handler),
            ],
            IMAGE_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Back$'), start),
                MessageHandler(filters.TEXT, pre_image_answer_handler),
            ],
            DALL_E_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Back$'), start),
                MessageHandler(filters.TEXT, pre_dall_e_answer_handler),
            ],
            INFO_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Back$'), start),
                MessageHandler(filters.Regex('^Buy tokens and generations$'), purchase),
            ],
            PURCHASE_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Back$'), display_info),
                MessageHandler(filters.Regex('^1 million ChatGPT tokens - 5 USDT$'), currencies),
                MessageHandler(filters.Regex('^100 DALL·E image generations - 5 USDT$'), currencies),
                MessageHandler(filters.Regex('^100 Stable Diffusion image generations - 5 USDT$'), currencies),
            ],
            PURCHASE_CHATGPT_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Back$'), purchase),
                MessageHandler(filters.Regex('^USDT$'), buy_chatgpt),
                MessageHandler(filters.Regex('^TON$'), buy_chatgpt),
                MessageHandler(filters.Regex('^BTC$'), buy_chatgpt),
                MessageHandler(filters.Regex('^ETH$'), buy_chatgpt),
            ],
            PURCHASE_DALL_E_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Back$'), purchase),
                MessageHandler(filters.Regex('^USDT$'), buy_dall_e),
                MessageHandler(filters.Regex('^TON$'), buy_dall_e),
                MessageHandler(filters.Regex('^BTC$'), buy_dall_e),
                MessageHandler(filters.Regex('^ETH$'), buy_dall_e),
            ],
            PURCHASE_STABLE_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Back$'), purchase),
                MessageHandler(filters.Regex('^USDT$'), buy_stable),
                MessageHandler(filters.Regex('^TON$'), buy_stable),
                MessageHandler(filters.Regex('^BTC$'), buy_stable),
                MessageHandler(filters.Regex('^ETH$'), buy_stable),
            ],
        },
        fallbacks=[],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(keyboard_callback))
    application.run_polling()
