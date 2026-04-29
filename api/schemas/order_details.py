from typing import Optional
from pydantic import BaseModel
from .sandwiches import Sandwich


class OrderDetailBase(BaseModel):
    amount: int


class OrderDetailCreate(OrderDetailBase):
    sandwich_id: int
    order_id: int


class OrderDetailUpdate(BaseModel):
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int
    sandwich: Sandwich

    class ConfigDict:
        from_attributes = True
