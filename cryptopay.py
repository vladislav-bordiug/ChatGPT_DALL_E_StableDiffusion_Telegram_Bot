from dotenv import load_dotenv
from aiocryptopay import AioCryptoPay, Networks, utils
from aiocryptopay.models.update import Update
from aiohttp import web
from os import getenv

load_dotenv()
web_app = web.Application()
crypto = AioCryptoPay(token=getenv("CRYPTOPAY_KEY"), network=Networks.MAIN_NET)

class CryptoPay:
    @crypto.pay_handler()
    async def invoice_paid(update: Update, app) -> None:
        print(update)

    async def getprice(cost: int, currency: str):
        rates = await crypto.get_exchange_rates()
        if currency == "USDT":
            pass
        elif currency == "TON":
            exchange = float((utils.exchange.get_rate('TON', 'USD', rates)).rate)
            cost = cost / exchange
        elif currency == "BTC":
            exchange = float((utils.exchange.get_rate('BTC', 'USD', rates)).rate)
            cost = cost / exchange
        elif currency == "ETH":
            exchange = float((utils.exchange.get_rate('ETH', 'USD', rates)).rate)
            cost = cost / exchange
        return cost

    async def create_invoice(cost: int, currency: str):
        price = await CryptoPay.getprice(cost, currency)
        invoice = await crypto.create_invoice(asset=currency, amount=price)
        return invoice.bot_invoice_url, invoice.invoice_id

    async def get_status(invoice_id: int):
        invoices = await crypto.get_invoices(invoice_ids=invoice_id)
        return invoices.status

web_app.add_routes([web.post('/crypto-secret-path', crypto.get_updates)])
web.run_app(app=web_app, host='localhost', port=3001)