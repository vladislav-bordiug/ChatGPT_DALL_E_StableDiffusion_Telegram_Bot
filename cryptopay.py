from dotenv import load_dotenv
from aiocryptopay import AioCryptoPay, Networks, utils
import os

class CryptoPay:
    def __init__(self):
        load_dotenv()
        self.crypto = AioCryptoPay(token=os.getenv("CRYPTOPAY_KEY"), network=Networks.TEST_NET)

    async def getprice(self, cost: int, currency: str):
        rates = await self.crypto.get_exchange_rates()
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

    async def create_invoice(self, cost: int, currency: str):
        price = await self.getprice(cost, currency)
        invoice = await self.crypto.create_invoice(asset=currency, amount=price)
        return invoice.bot_invoice_url, invoice.invoice_id

    async def get_status(self, invoice_id: int):
        invoices = await self.crypto.get_invoices(invoice_ids=invoice_id)
        return invoices.status