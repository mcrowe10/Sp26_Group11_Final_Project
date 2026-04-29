from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CreatePromotion(BaseModel):
    promotion_code: str
    discount: float
    expire_date: Optional[datetime] = None

class UpdatePromotion(BaseModel):
    discount: Optional[float] = None
    is_active: Optional[bool] = None
    expire_date: Optional[datetime] = None

class Promotion(BaseModel):
    promotion_id: int
    promotion_code: str
    discount: float
    is_active: bool
    expire_date: Optional[datetime] = None

    class Config:
        from_attributes = True