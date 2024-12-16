from pydantic import BaseModel

class InvoicePayload(BaseModel):
    invoice_id: int

class PaymentsRequestModel(BaseModel):
    update_type: str
    payload: InvoicePayload