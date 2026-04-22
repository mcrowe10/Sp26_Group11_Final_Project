from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .customers import Customer


class ReviewBase(BaseModel):
    score: float


class ReviewCreate(ReviewBase):
    customer_id: int


class ReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    score: Optional[float] = None


class Review(ReviewBase):
    id: int
    review_text: str
    customer: Optional[Customer] = None

    class ConfigDict:
        from_attributes = True
