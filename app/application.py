import os
from dotenv import load_dotenv

from fastapi import FastAPI, APIRouter
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage

from app.services.db import DataBase
from app.services.cryptopay import CryptoPay
from app.services.openaitools import OpenAiTools
from app.services.stablediffusion import StableDiffusion
from app.core.database import DataBaseCore
from app.bot.setup import register_handlers
from app.api.setup import register_routes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL") + TOKEN

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

storage = RedisStorage.from_url(os.getenv("REDIS_URL"))

dp = Dispatcher(storage=storage)

db_core = DataBaseCore(os.getenv("DATABASE_URL"))
database = DataBase(db_core.pool)
cryptopay = CryptoPay(os.getenv("CRYPTOPAY_KEY"))
openai_tools = OpenAiTools(os.getenv("OPENAI_API_KEY"))
stable = StableDiffusion(os.getenv("STABLE_DIFFUSION_API_KEY"))

register_handlers(dp, database, openai_tools, stable, cryptopay)

app = FastAPI()

router = APIRouter()

register_routes(router, database, dp, bot, os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("CRYPTOPAY_KEY"))

app.include_router(router)


def on_startup_handler(database_core: DataBaseCore, database: DataBase):
    async def on_startup() -> None:
        await database_core.open_pool()
        await database.create_tables()
        lockfile = "/tmp/.webhook_registered"
        try:
            fd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w") as f:
                f.write(str(os.getpid()))
            await bot.set_webhook(url=WEBHOOK_URL)
        except FileExistsError:
            pass
    return on_startup

app.add_event_handler("startup", on_startup_handler(db_core, database))


def on_shutdown_handler():
    async def on_shutdown() -> None:
        await bot.delete_webhook()
        await bot.session.close()
    return on_shutdown

app.add_event_handler("shutdown", on_shutdown_handler())