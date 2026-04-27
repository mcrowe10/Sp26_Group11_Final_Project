from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .customers import Customer


class ReviewBase(BaseModel):
    score: float
    review_text: str


class ReviewCreate(ReviewBase):
    customer_id: int


class ReviewUpdate(BaseModel):
    score: Optional[float] = None
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int
    customer: Optional[Customer] = None

    class ConfigDict:
        from_attributes = True
