#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import python-telegram-bot
import requests
import deep_translator
from deep_translator import GoogleTranslator
  
import os

from copilot import Copilot
from text_to_image import TextToImage
from dotenv import load_dotenv

from telegram import (
    ReplyKeyboardMarkup,
    Update,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    )

(ENTRY_STATE, 
QUESTION_STATE,
IMAGE_STATE, ) = range(3)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vercel_app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


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
  
async def start(update: Update, context: ContextTypes):
    """Start the conversation and ask user for an option."""

    button = [[KeyboardButton(text="Question-Answering — ChatGPT 3.5 Turbo")], [KeyboardButton(text="Image generation — Stable Diffusion")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Choose an option: 👇🏻",
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
  
#Handling the answer
async def pre_query_answer_handler(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    question = update.message.text

    answer = _generate_copilot(question)

    context.user_data['answer'] = answer

    await update.message.reply_text(
        answer, 
        reply_markup=reply_markup,
    )

    return QUESTION_STATE

async def pre_image_answer_handler(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    question = update.message.text
    print(question)

    en_v = _translate(question)
    print(en_v)

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

    return IMAGE_STATE
  
if __name__ == '__main__':
    load_dotenv()

    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).read_timeout(100).get_updates_read_timeout(100).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),MessageHandler(filters.Regex('^Question-Answering — ChatGPT 3.5 Turbo$'), pre_query_handler),MessageHandler(filters.Regex('^Image generation — Stable Diffusion$'), pre_image_handler),MessageHandler(filters.Regex('^Back$'), start)],
        states={
            ENTRY_STATE: [
                CommandHandler('start', start),
                MessageHandler(filters.Regex('^Back$'), start),
                MessageHandler(filters.Regex('^Question-Answering — ChatGPT 3.5 Turbo$'), pre_query_handler),
                MessageHandler(filters.Regex('^Image generation — Stable Diffusion$'), pre_image_handler),
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
        },
        fallbacks=[],
    )
    
    application.add_handler(conv_handler)
    application.run_polling()
