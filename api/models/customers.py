from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    email = Column(String(100))
    phone_number = Column(Integer)
    address = Column(String(100))
    default_payment = Column(Integer, ForeignKey("payments.id"))

    orders = relationship("Order", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")