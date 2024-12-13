from os import getenv

from db import DataBase

from dotenv import load_dotenv

import os

from fastapi import FastAPI, Request, APIRouter
import uvicorn

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from app.bot.setup import register_handlers

from app.api.setup import register_routes

dp = Dispatcher()
app = FastAPI()

async def on_startup() -> None:
    await DataBase.open_pool()
    url_webhook = getenv("BASE_WEBHOOK_URL") + getenv("TELEGRAM_BOT_TOKEN")
    await bot.set_webhook(url=url_webhook)

if __name__ == '__main__':
    load_dotenv()

    register_handlers(dp)

    bot = Bot(token=getenv("TELEGRAM_BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    router = APIRouter()

    register_routes(router, dp, bot)

    app.include_router(router)

    app.add_event_handler("startup", on_startup)

    uvicorn.run(app, host=getenv("0.0.0.0"), port=int(os.environ.get("PORT", 5000)))
