from aiogram import Bot
from fastapi import Request
from fastapi.responses import PlainTextResponse
from db import DataBase

async def payments_webhook(request: Request, bot: Bot) -> PlainTextResponse:
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