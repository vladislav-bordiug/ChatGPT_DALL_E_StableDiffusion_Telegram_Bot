from fastapi import APIRouter
from app.api.routes.telegram import bot_webhook
from app.api.routes.cryptopay import payments_webhook
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from os import getenv

def register_routes(router: APIRouter, dp: Dispatcher, bot: Bot, telegram_token: str, cryptopay_token: str):
    async def telegram_webhook(request):
        return await bot_webhook(request, dp, bot)

    async def cryptopay_webhook(request):
        return await payments_webhook(request, bot)

    load_dotenv()

    print(telegram_token)

    router.add_api_route("/" + telegram_token, telegram_webhook, methods=["POST"])
    router.add_api_route("/" + cryptopay_token, cryptopay_webhook, methods=["POST"])