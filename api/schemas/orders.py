from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .payments import Payment
from .customers import Customer


class OrderBase(BaseModel):
    order_date: datetime
    tracking_number: str
    order_status: str
    price: float


class OrderCreate(OrderBase):
    customer_id: int
    payment_status: str


class OrderUpdate(BaseModel):
    description: Optional[str] = None
    order_status: Optional[str] = None
    tracking_number: Optional[str] = None
    price: Optional[float] = None


class Order(OrderBase):
    id: int
    customer_id: int
    description: str
    customer: Optional[Customer] = None
    payment: Payment = None


    class ConfigDict:
        from_attributes = True
