from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .payments import Payment


class CustomerBase(BaseModel):
    customer_name: str
    default_payment: Optional[int] = None
    payment: Optional[Payment] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    default_payment: Optional[int] = None


class Customer(CustomerBase):
    id: int
    email: str
    phone_number: str
    address: str

    class ConfigDict:
        from_attributes = True