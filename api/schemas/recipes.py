from typing import Optional
from pydantic import BaseModel
from .resources import Resource


class RecipeBase(BaseModel):
    amount: int


class RecipeCreate(RecipeBase):
    sandwich_id: int
    resource_id: int


class RecipeUpdate(BaseModel):
    amount: Optional[int] = None


class Recipe(RecipeBase):
    id: int
    resource: Resource

    class ConfigDict:
        from_attributes = True
