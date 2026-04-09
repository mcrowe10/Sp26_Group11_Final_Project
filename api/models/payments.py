from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_info = Column(String, index=True, nullable=False)
    status = Column(String(50), index=True, nullable=False)
    payment_type = Column(String(50), index=True, nullable=False)

    customer = relationship("Customer", back_populates="payments")
    orders = relationship("Orders", back_populates="payments")