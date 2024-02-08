from dotenv import load_dotenv
from aiocryptopay import AioCryptoPay, Networks, utils
from os import getenv

load_dotenv()
crypto = AioCryptoPay(token=getenv("CRYPTOPAY_KEY"), network=Networks.MAIN_NET)

class CryptoPay:
    async def getprice(cost: int, currency: str):
        rates = await crypto.get_exchange_rates()
        if currency == "USDT":
            exchange = float((utils.exchange.get_rate('USDT', 'USD', rates)).rate)
            cost = cost / exchange
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