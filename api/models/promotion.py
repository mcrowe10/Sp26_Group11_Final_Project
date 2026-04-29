from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotion"

    promotion_id = Column(Integer, primary_key = True, index = True)
    promotion_code = Column(String, unique = True, index = True)
    discount = Column(Float)
    is_active = Column(Boolean, default = True)
    expire_date = Column(DateTime, nullable = True)