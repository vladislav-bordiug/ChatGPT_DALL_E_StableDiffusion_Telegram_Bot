import os
from aiocryptopay import AioCryptoPay, Networks
from dotenv import load_dotenv
load_dotenv()

class Payment:
    async def payment(self, currency, cost):
        crypto = AioCryptoPay(token=os.getenv("CRYPTOPAY_KEY"), network=Networks.MAIN_NET)
        
        invoice = await crypto.create_invoice(asset=currency, amount=cost)
            return invoice

    async def check_payment(self,invoice):
        invoices = await crypto.get_invoices(invoice_ids=invoice.invoice_id)
        return invoices.status
