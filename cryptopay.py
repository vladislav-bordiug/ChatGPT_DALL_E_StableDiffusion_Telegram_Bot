import os
from aiohttp import web

from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update
load_dotenv()

web_app = web.Application()
crypto = AioCryptoPay(token=os.getenv("CRYPTOPAY_KEY"), network=Networks.MAIN_NET)


@crypto.pay_handler()
async def invoice_paid(update: Update) -> None:
    return update

async def create_invoice(app) -> None:
    invoice = await crypto.create_invoice(asset='TON', amount=1.5)
    print(invoice.pay_url)

async def close_session(app) -> None:
    await crypto.close()


web_app.add_routes([web.post(os.getenv("SECRET_DOMAIN"), crypto.get_updates)])
web_app.on_startup.append(create_invoice)
web_app.on_shutdown.append(close_session)
web.run_app(app=web_app, host='localhost', port=3001)
