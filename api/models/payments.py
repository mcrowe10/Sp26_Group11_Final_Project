from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_info = Column(String(100))
    status = Column(String(50), server_default="pending")
    payment_type = Column(String(50), server_default="CreditCard")

    customer = relationship("Customer", back_populates="payment")