from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    review_text = Column(String(300), nullable=True, server_default="")
    score = Column(DECIMAL(4,2), nullable=False, server_default='0.0')

    customer = relationship("Customer", back_populates="reviews")