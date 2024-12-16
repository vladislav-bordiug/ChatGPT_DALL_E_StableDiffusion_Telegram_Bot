from fastapi import APIRouter
from app.api.routes.routes import Handlers
from aiogram import Bot, Dispatcher
from app.services.db import DataBase


def register_routes(router: APIRouter, database: DataBase, dp: Dispatcher, bot: Bot, telegram_token: str, cryptopay_token: str):
    routes_class = Handlers(database, dp, bot)

    router.add_route("/" + telegram_token, routes_class.bot_webhook, methods=["POST"])
    router.add_route("/" + cryptopay_token, routes_class.payments_webhook, methods=["POST"])