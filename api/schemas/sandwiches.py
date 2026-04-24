from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .recipes import Recipe


class SandwichBase(BaseModel):
    sandwich_name: str
    price: float


class SandwichCreate(SandwichBase):
    calories: int
    food_category: str


class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    food_category: Optional[str] = None


class Sandwich(SandwichBase):
    id: int
    recipe: List[Recipe] = []

    class ConfigDict:
        from_attributes = True