from fastapi import APIRouter
from app.api.routes.telegram import bot_webhook
from app.api.routes.cryptopay import payments_webhook
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from os import getenv

def register_routes(router: APIRouter, dp: Dispatcher, bot: Bot):
    async def telegram_webhook(request):
        return await bot_webhook(request, dp, bot)

    async def cryptopay_webhook(request):
        return await payments_webhook(request, bot)

    load_dotenv()

    router.add_api_route("/" + getenv("TELEGRAM_BOT_TOKEN"), telegram_webhook, methods=["POST"])
    router.add_api_route("/" + getenv("CRYPTOPAY_KEY"), cryptopay_webhook, methods=["POST"])