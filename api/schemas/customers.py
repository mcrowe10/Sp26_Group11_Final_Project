from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .payments import Payment


class CustomerBase(BaseModel):
    customer_name: str



class CustomerCreate(CustomerBase):
    default_payment_id: int


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    default_payment_id: Optional[int] = None


class Customer(CustomerBase):
    id: int
    email: str
    phone_number: str
    address: str
    payment: Optional[Payment] = None

    class ConfigDict:
        from_attributes = True