from typing import Optional
from pydantic import BaseModel
from .payments import PaymentCreate, Payment


class CustomerBase(BaseModel):
    customer_name: str


class CustomerCreate(CustomerBase):
    payment_id: Optional[int] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    default_payment: Optional[PaymentCreate] = None


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    payment_id: Optional[int] = None


class Customer(CustomerBase):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    id: int
    default_payment: Optional[Payment] = None

    class ConfigDict:
        from_attributes = True


class CustomerDisplay(CustomerBase):

    class ConfigDict:
        from_attributes = True
