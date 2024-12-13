from aiogram import Bot
from fastapi import Request
from fastapi.responses import PlainTextResponse
from app.services.db import DataBase
from app.services.payment_successful import payment_success

async def payments_webhook(request: Request, bot: Bot, database: DataBase) -> PlainTextResponse:
    data = await request.json()
    update_type = data['update_type']
    invoice = data['payload']
    invoice_id = int(invoice['invoice_id'])
    await payment_success(bot, database, update_type, invoice_id)
    return PlainTextResponse('OK', status_code=200)