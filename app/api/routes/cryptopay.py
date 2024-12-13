from aiogram import Bot
from fastapi import Request
from fastapi.responses import PlainTextResponse

from app.bot.utils import TelegramError
from app.services.db import DataBase, DatabaseError
from app.services.payment_successful import payment_success

async def payments_webhook(request: Request, bot: Bot, database: DataBase) -> PlainTextResponse:
    try:
        data = await request.json()
        if 'update_type' not in data or 'payload' not in data or 'invoice_id' not in data['payload']:
            return PlainTextResponse('Wrong request', status_code=400)
        update_type = data['update_type']
        invoice = data['payload']
        try:
            invoice_id = int(invoice['invoice_id'])
        except ValueError:
            return PlainTextResponse('Wrong invoice_id', status_code=400)
        await payment_success(bot, database, update_type, invoice_id)
        return PlainTextResponse('OK', status_code=200)
    except DatabaseError:
        return PlainTextResponse('Database Error', status_code=500)
    except TelegramError:
        return PlainTextResponse('Telegram Error', status_code=500)
    except Exception:
        return PlainTextResponse('Error', status_code=500)