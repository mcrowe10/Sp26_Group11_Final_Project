from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .customers import Customer



class ReviewBase(BaseModel):
    review_text: str
    score: float = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    customer_name: Optional[str] = None


class Review(ReviewBase):
    id: int
    customer_name: list[Customer] = None

    class ConfigDict:
        from_attributes = True
