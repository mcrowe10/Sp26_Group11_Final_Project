from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .customers import Customer
from .order_details import OrderDetail


class OrderBase(BaseModel):
    order_date: datetime
    customer_name: str
    description: str
    order_status: str
    tracking_number: str


class OrderCreate(OrderBase):
    customer_id: int


class OrderUpdate(BaseModel):
    description: Optional[str] = None
    order_status: Optional[str] = None
    tracking_number: Optional[str] = None
    price: Optional[float] = None


class Order(OrderBase):
    id: int
    price: float
    customer: Optional[Customer] = None
    order_details: List[OrderDetail] = []


    class ConfigDict:
        from_attributes = True
