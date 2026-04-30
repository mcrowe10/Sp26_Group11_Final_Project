from typing import Optional
from pydantic import BaseModel
from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "Pending"
    SAVED = "Default"
    SUCCESS = "Complete"


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
    status: PaymentStatus
    id: int

    class ConfigDict:
        from_attributes = True
