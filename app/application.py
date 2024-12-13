from os import getenv

from app.services.db import DataBase
from app.services.cryptopay import CryptoPay
from app.services.openaitools import OpenAiTools
from app.services.stablediffusion import StableDiffusion

from dotenv import load_dotenv

import os

from fastapi import FastAPI, APIRouter
import uvicorn

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from app.bot.setup import register_handlers

from app.api.setup import register_routes

from app.core.database import DataBaseCore

dp = Dispatcher()
app = FastAPI()

def run():
    load_dotenv()

    cryptopay = CryptoPay(getenv("CRYPTOPAY_KEY"))

    database_core = DataBaseCore(getenv("DATABASE_URL"))

    database = DataBase(database_core.pool)

    openai = OpenAiTools(getenv("OPENAI_API_KEY"))

    stable = StableDiffusion(getenv("STABLE_DIFFUSION_API_KEY"))

    register_handlers(dp, database, openai, stable, cryptopay)

    bot = Bot(token=getenv("TELEGRAM_BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    router = APIRouter()

    register_routes(router, database, dp, bot, getenv("TELEGRAM_BOT_TOKEN"), getenv("CRYPTOPAY_KEY"))

    app.include_router(router)


    def on_startup_handler(database_core: DataBaseCore):
        async def on_startup() -> None:
            await database_core.open_pool()
            url_webhook = getenv("BASE_WEBHOOK_URL") + getenv("TELEGRAM_BOT_TOKEN")
            await bot.set_webhook(url=url_webhook)

        return on_startup

    app.add_event_handler("startup", on_startup_handler(database_core))

    uvicorn.run(app, host=getenv("0.0.0.0"), port=int(os.environ.get("PORT", 5000)))
