from fastapi import APIRouter, Request
from app.api.routes.telegram import bot_webhook
from app.api.routes.cryptopay import payments_webhook
from aiogram import Bot, Dispatcher

def register_routes(router: APIRouter, dp: Dispatcher, bot: Bot, telegram_token: str, cryptopay_token: str):
    async def telegram_webhook(request: Request):
        return await bot_webhook(request, dp, bot)

    async def cryptopay_webhook(request: Request):
        return await payments_webhook(request, bot)

    router.add_route("/" + telegram_token, telegram_webhook, methods=["POST"])
    router.add_route("/" + cryptopay_token, cryptopay_webhook, methods=["POST"])