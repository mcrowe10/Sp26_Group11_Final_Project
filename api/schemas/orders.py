from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail
from .payments import Payment


class OrderBase(BaseModel):
    order_date: datetime
    customer_name: str
    description: Optional[str] = None
    order_status: str
    tracking_number: str
    payment: Payment = None


class OrderCreate(OrderBase):
    customer_id: Optional[int] = None


class OrderUpdate(BaseModel):
    description: Optional[str] = None
    order_status: Optional[str] = None


class Order(OrderBase):
    price: float
    id: int
    order_details: List[OrderDetail] = []

    class ConfigDict:
        from_attributes = True
