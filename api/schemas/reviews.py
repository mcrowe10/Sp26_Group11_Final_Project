from typing import Optional
from pydantic import BaseModel
from .customers import CustomerDisplay


class ReviewBase(BaseModel):
    score: float
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    customer_id: int


class ReviewUpdate(BaseModel):
    score: Optional[float] = None
    review_text: Optional[str] = None


class Review(ReviewBase):
    customer: CustomerDisplay
    id: int

    class ConfigDict:
        from_attributes = True
