from aiogram import Bot, Dispatcher, types
from fastapi import Request
from fastapi.responses import JSONResponse

async def bot_webhook(request: Request, dp: Dispatcher, bot: Bot) -> JSONResponse:
    update = types.Update(**await request.json())
    await dp.feed_webhook_update(bot, update)
    return JSONResponse(content={"status": "ok"})