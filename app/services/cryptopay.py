from aiocryptopay import AioCryptoPay, Networks, utils
import logging

class CryptoPayError(Exception):
    def __init__(self, msg: str = "Error"):
        self.msg=msg
    def output(self):
        logging.error("CryptoPay error:", self.msg)

class CryptoPay:
    def __init__(self, token: str):
        self.crypto = AioCryptoPay(token=token, network=Networks.MAIN_NET)
    async def getprice(self, cost: int, currency: str):
        try:
            rates = await self.crypto.get_exchange_rates()
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
        except Exception as e:
            err = CryptoPayError(str(e))
            err.output()
            raise err

    async def create_invoice(self, cost: int, currency: str):
        try:
            price = await self.getprice(cost, currency)
            invoice = await self.crypto.create_invoice(asset=currency, amount=price)
            return invoice.bot_invoice_url, invoice.invoice_id
        except Exception as e:
            err = CryptoPayError(str(e))
            err.output()
            raise err