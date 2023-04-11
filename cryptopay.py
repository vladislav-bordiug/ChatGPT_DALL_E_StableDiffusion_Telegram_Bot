import os
from aiocryptopay import AioCryptoPay, Networks
from dotenv import load_dotenv
load_dotenv()

class Payment:
    async def payment(self):
        crypto = AioCryptoPay(token=os.getenv("CRYPTOPAY_KEY"), network=Networks.MAIN_NET)
        
        invoice = await crypto.create_invoice(asset='TON', amount=1.5)
        print(invoice.pay_url)

        invoices = await crypto.get_invoices(invoice_ids=invoice.invoice_id)
        print("dsdfsfds",invoices.status)
