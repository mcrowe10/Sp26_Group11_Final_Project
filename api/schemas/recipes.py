from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource


class RecipeBase(BaseModel):
    amount: int
    sandwich_id: int


class RecipeCreate(RecipeBase):
    resource_id: int

class RecipeUpdate(BaseModel):
    amount: Optional[int] = None
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    resource: Resource = None

    class ConfigDict:
        from_attributes = True