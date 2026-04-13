from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    score: float


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    score: Optional[float] = None
    customer_name: Optional[str] = None


class Review(ReviewBase):
    id: int
    review_text: str
    customer_name: str

    class ConfigDict:
        from_attributes = True
