from typing import Optional
from pydantic import BaseModel
from .payments import Payment


class CustomerBase(BaseModel):
    customer_name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    payment: Optional[Payment] = None


class CustomerCreate(CustomerBase):
    default_payment: Optional[int] = None


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    default_payment: Optional[int] = None


class Customer(CustomerBase):
    id: int

    class ConfigDict:
        from_attributes = True
