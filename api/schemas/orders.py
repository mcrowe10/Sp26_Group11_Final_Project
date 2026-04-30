from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail
from .payments import Payment
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "Pending"
    PAID = "Paid"
    SUCCESS = "Complete"


class OrderBase(BaseModel):
    order_date: datetime
    customer_name: str
    description: Optional[str] = None
    tracking_number: str


class OrderCreate(OrderBase):
    customer_id: Optional[int] = None
    payment_id: Optional[int] = None


class OrderUpdate(BaseModel):
    description: Optional[str] = None
    order_status: Optional[str] = None


class Order(OrderBase):
    price: float
    discounted_price: Optional[float] = None
    order_status: OrderStatus
    id: int
    order_details: List[OrderDetail] = []
    payment: Optional[Payment] = None

    class ConfigDict:
        from_attributes = True
