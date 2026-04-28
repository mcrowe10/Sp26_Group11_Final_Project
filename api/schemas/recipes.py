from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource, ResourceDisplay


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
    resource: ResourceDisplay = None

    class ConfigDict:
        from_attributes = True


class RecipeDisplay(BaseModel):
    amount: int
    resource: ResourceDisplay = None

    class ConfigDict:
        from_attributes = True