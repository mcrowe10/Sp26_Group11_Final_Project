from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PaymentStatus(str):
    pending = "pending"
    processing = "processing"
    complete = "complete"
    declined = "declined"


class PaymentBase(BaseModel):
    card_info: str
    payment_type: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    card_info: Optional[str] = None
    payment_type: Optional[str] = None
    status: Optional[str] = None


class Payment(PaymentBase):
    id: int
    status: str

    class ConfigDict:
        from_attributes = True