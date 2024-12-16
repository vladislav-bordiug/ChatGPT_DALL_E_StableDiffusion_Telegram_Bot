import pytest
from unittest.mock import AsyncMock

from app.services.cryptopay import CryptoPay

class Rate:
    def __init__(self, source, target, rate):
        self.source = source
        self.target = target
        self.rate = rate

class Invoice:
    def __init__(self, bot_invoice_url, invoice_id):
        self.bot_invoice_url = bot_invoice_url
        self.invoice_id = invoice_id

class TestGetPrice:
    @pytest.mark.asyncio
    async def test_getprice_success(self):
        crypto = CryptoPay('token')
        crypto.crypto = AsyncMock()

        crypto.crypto.get_exchange_rates = AsyncMock()

        rate = Rate('TON', 'USD', 1)
        crypto.crypto.get_exchange_rates.return_value = [rate]

        cost = await crypto.getprice(5, 'TON')

        crypto.crypto.get_exchange_rates.assert_awaited_once_with()

        assert cost == 5

    @pytest.mark.asyncio
    async def test_getprice_cryptopay_error(self):
        crypto = CryptoPay('token')
        crypto.crypto = AsyncMock()

        crypto.crypto.get_exchange_rates = AsyncMock()

        crypto.crypto.get_exchange_rates.side_effect = Exception()

        with pytest.raises(Exception):
            _ = await crypto.getprice(5, 'TON')

class TestCreateInvoice:
    @pytest.mark.asyncio
    async def test_create_invoice_success(self):
        crypto = CryptoPay('token')
        crypto.crypto = AsyncMock()
        crypto.getprice = AsyncMock()
        crypto.getprice.return_value = 5

        crypto.crypto.create_invoice = AsyncMock()

        invoice = Invoice('url', 1)
        crypto.crypto.create_invoice.return_value = invoice

        invoice_url, invoice_id = await crypto.create_invoice(5, 'TON')

        crypto.getprice.assert_awaited_once_with(5, 'TON')
        crypto.crypto.create_invoice.assert_awaited_once_with(asset='TON', amount=5)

        assert invoice_url == 'url'
        assert invoice_id == 1

    @pytest.mark.asyncio
    async def test_create_invoice_cryptopay_error(self):
        crypto = CryptoPay('token')
        crypto.crypto = AsyncMock()
        crypto.getprice = AsyncMock()
        crypto.getprice.side_effect = Exception()

        with pytest.raises(Exception):
            _, _ = await crypto.create_invoice(5, 'TON')

        crypto.getprice.assert_awaited_once_with(5, 'TON')