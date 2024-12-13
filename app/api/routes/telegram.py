from aiogram import Bot, Dispatcher, types
from fastapi import Request
from fastapi.responses import JSONResponse

from app.bot.utils import TelegramError
from app.services.cryptopay import CryptoPayError
from app.services.db import DatabaseError


async def bot_webhook(request: Request, dp: Dispatcher, bot: Bot) -> JSONResponse:
    try:
        update = types.Update(**await request.json())
        await dp.feed_webhook_update(bot, update)
        return JSONResponse(content={"status": "ok"})
    except DatabaseError:
        return JSONResponse(content={"message": "database error"}, status_code=500)
    except CryptoPayError:
        return JSONResponse(content={"message": "cryptopay error"}, status_code=500)
    except TelegramError:
        return JSONResponse(content={"message": "telegram error"}, status_code=500)
    except Exception:
        return JSONResponse(content={"message": "error"}, status_code=500)