from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    customer_id: int
    score: float
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    score: Optional[float] = None
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True
