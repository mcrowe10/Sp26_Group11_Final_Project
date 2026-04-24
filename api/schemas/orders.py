from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .payments import Payment
from .customers import Customer
from .order_details import OrderDetail


class OrderBase(BaseModel):
    order_date: datetime
    tracking_number: str
    order_status: str
    price: float


class OrderCreate(OrderBase):
    customer_id: int


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
    order_details: List[OrderDetail] = []


    class ConfigDict:
        from_attributes = True
