from fastapi import APIRouter
from app.api.routes.telegram import bot_webhook
from app.api.routes.cryptopay import payments_webhook
from aiogram import Bot, Dispatcher

def register_routes(router: APIRouter, dp: Dispatcher, bot: Bot, telegram_token: str, cryptopay_token: str):
    async def telegram_webhook(request):
        raw_body = await request.body()

        body_text = raw_body.decode("utf-8")

        print("Request body:", body_text)

        return await bot_webhook(request, dp, bot)

    async def cryptopay_webhook(request):
        return await payments_webhook(request, bot)

    router.add_route("/" + telegram_token, telegram_webhook, methods=["POST"])
    router.add_route("/" + cryptopay_token, cryptopay_webhook, methods=["POST"])