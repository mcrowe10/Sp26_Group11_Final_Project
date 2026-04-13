from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PromotionBase(BaseModel):
    id: int


class PromotionCreate(PromotionBase):
    promo_code: str
    expiration_date: datetime

class PromotionUpdate(BaseModel):
    promo_code: Optional[str] = None
    expiration_date: Optional[datetime] = None

class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True