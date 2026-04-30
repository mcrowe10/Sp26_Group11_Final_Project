from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_info = Column(String(100))
    status = Column(String(50))
    payment_type = Column(String(50))

    customer = relationship("Customer", back_populates="default_payment")
    orders = relationship("Order", back_populates="payment")