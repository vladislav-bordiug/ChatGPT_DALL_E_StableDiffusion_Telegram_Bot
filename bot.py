from os import getenv

from db import DataBase

from app.bot.setup import register_handlers

from dotenv import load_dotenv

import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import uvicorn

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties


dp = Dispatcher()
app = FastAPI()

# Processes message
@app.post("/" + getenv("TELEGRAM_BOT_TOKEN"))
async def bot_webhook(request: Request) -> JSONResponse:
    update = types.Update(**await request.json())
    await dp.feed_webhook_update(bot, update)
    return JSONResponse(content={"status": "ok"})

# Checks payment
@app.post("/" + getenv("CRYPTOPAY_KEY"))
async def payments_webhook(request: Request) -> PlainTextResponse:
    data = await request.json()
    update_type = data['update_type']
    if update_type == "invoice_paid":
        invoice = data['payload']
        invoice_id = invoice['invoice_id']
        result = await DataBase.get_orderdata(invoice_id)
        if result[1] == 'chatgpt':
            await DataBase.update_chatgpt(result[0], invoice_id)
            await bot.send_message(result[0], "✅You have received 100000 ChatGPT tokens!")
        elif result[1] == 'dall_e':
            await DataBase.update_dalle(result[0], invoice_id)
            await bot.send_message(result[0], "✅You have received 50 DALL·E image generations!")
        elif result[1] == 'stable':
            await DataBase.update_stable(result[0], invoice_id)
            await bot.send_message(result[0], "✅You have received 50 Stable Diffusion image generations!")
    return PlainTextResponse('OK', status_code=200)

async def on_startup() -> None:
    await DataBase.open_pool()
    url_webhook = getenv("BASE_WEBHOOK_URL") + getenv("TELEGRAM_BOT_TOKEN")
    await bot.set_webhook(url=url_webhook)

if __name__ == '__main__':
    load_dotenv()

    register_handlers(dp)

    bot = Bot(token=getenv("TELEGRAM_BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    app.add_event_handler("startup", on_startup)

    uvicorn.run(app, host=getenv("0.0.0.0"), port=int(os.environ.get("PORT", 5000)))
