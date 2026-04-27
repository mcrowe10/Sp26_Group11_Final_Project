from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .recipes import Recipe


class SandwichBase(BaseModel):
    sandwich_name: str
    food_category: str
    calories: int
    price: float


class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    food_category: Optional[str] = None
    calories: Optional[int] = None
    price: Optional[float] = None


class Sandwich(SandwichBase):
    id: int
    recipe: List[Recipe] = []

    class ConfigDict:
        from_attributes = True