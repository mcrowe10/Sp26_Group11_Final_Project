from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .payments import DisplayPayment


class CustomerBase(BaseModel):
    customer_name: str


class CustomerCreate(CustomerBase):
    default_payment: Optional[int] = None
    payment: Optional[DisplayPayment] = None


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    default_payment: Optional[int] = None


class Customer(CustomerBase):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    payment: Optional[DisplayPayment] = None
    id: int

    class ConfigDict:
        from_attributes = True


class DisplayCustomer(CustomerBase):

    class ConfigDict:
        from_attributes = True