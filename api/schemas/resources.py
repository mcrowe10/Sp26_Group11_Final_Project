from typing import Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    item: str


class ResourceCreate(ResourceBase):
    amount: int


class ResourceUpdate(BaseModel):
    item: Optional[str] = None
    amount: Optional[int] = None


class Resource(ResourceBase):
    amount: int
    id: int

    class ConfigDict:
        from_attributes = True


class ResourceDisplay(ResourceBase):

    class ConfigDict:
        from_attributes = True
