from aiogram import Bot, Dispatcher, types
from fastapi import Request
from fastapi.responses import PlainTextResponse, JSONResponse

from app.bot.utils import TelegramError
from app.services.cryptopay import CryptoPayError
from app.services.db import DataBase, DatabaseError
from app.services.payment_successful import payment_success
import logging

class Handlers:
    def __init__(self, database: DataBase, dp: Dispatcher, bot: Bot):
        self.database = database
        self.dp = dp
        self.bot = bot

    async def payments_webhook(self, request: Request) -> PlainTextResponse:
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
            await payment_success(self.bot, self.database, update_type, invoice_id)
            return PlainTextResponse('OK', status_code=200)
        except DatabaseError:
            return PlainTextResponse('Database Error', status_code=500)
        except TelegramError:
            return PlainTextResponse('Telegram Error', status_code=500)
        except Exception as e:
            logging.exception(e)
            return PlainTextResponse('Error', status_code=500)

    async def bot_webhook(self, request: Request) -> JSONResponse:
        try:
            update = types.Update(**await request.json())
            await self.dp.feed_webhook_update(self.bot, update)
            return JSONResponse(content={"status": "ok"})
        except DatabaseError:
            return JSONResponse(content={"message": "database error"}, status_code=500)
        except CryptoPayError:
            return JSONResponse(content={"message": "cryptopay error"}, status_code=500)
        except TelegramError:
            return JSONResponse(content={"message": "telegram error"}, status_code=500)
        except Exception as e:
            logging.exception(e)
            return JSONResponse(content={"message": "error"}, status_code=500)