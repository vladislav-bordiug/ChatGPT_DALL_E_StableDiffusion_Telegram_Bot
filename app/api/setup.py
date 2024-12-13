from fastapi import APIRouter
from app.api.routes.telegram import bot_webhook
from app.api.routes.cryptopay import payments_webhook
from aiogram import Bot, Dispatcher
from urllib.parse import quote

def register_routes(router: APIRouter, dp: Dispatcher, bot: Bot, telegram_token: str, cryptopay_token: str):
    async def telegram_webhook(request):
        return await bot_webhook(request, dp, bot)

    async def cryptopay_webhook(request):
        return await payments_webhook(request, bot)

    telegram_token = quote(telegram_token)
    cryptopay_token = quote(cryptopay_token)
    print(telegram_token)

    router.add_api_route("/" + telegram_token, telegram_webhook, methods=["POST"])
    router.add_api_route("/" + cryptopay_token, cryptopay_webhook, methods=["POST"])