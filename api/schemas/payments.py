from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .orders import Order
from .customers import Customer

class PaymentBase(BaseModel):
    amount: int


class PaymentCreate(PaymentBase):
    card_info: str
    status: str

class PaymentUpdate(BaseModel):
    card_info: Optional[str] = None
    status: Optional[str] = None
    payment_type: Optional[str] = None

class Payment(PaymentBase):
    id: int
    customer: Customer = None
    order: Order = None

    class ConfigDict:
        from_attributes = True