from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .payments import Payment
from .customers import Customer


class OrderBase(BaseModel):
    order_date: datetime


class OrderCreate(OrderBase):
    customer_name: str
    payment_status: str


class OrderUpdate(BaseModel):
    description: Optional[str] = None
    order_status: Optional[str] = None
    tracking_number: Optional[str] = None
    price: Optional[float] = None


class Order(OrderBase):
    id: int
    description: str
    order_status: str
    tracking_number: int
    price: float
    customer: Customer = None
    payment: Payment = None


    class ConfigDict:
        from_attributes = True
