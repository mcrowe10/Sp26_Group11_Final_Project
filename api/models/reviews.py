from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    review_text = Column(String, index=True, nullable=False)
    score = Column(DECIMAL(4,2), nullable=False)

    customers = relationship("Customer", back_populates="reviews")