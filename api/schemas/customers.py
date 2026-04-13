from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CustomerBase(BaseModel):
    customer_name: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    default_payment_method: Optional[str] = None


class Customer(CustomerBase):
    id: int

    class ConfigDict:
        from_attributes = True