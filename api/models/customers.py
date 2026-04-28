from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), unique=True)
    email = Column(String(100), nullable=True)
    phone_number = Column(String(100), nullable=True)
    address = Column(String(100), nullable=True)
    default_payment= Column(Integer, ForeignKey("payments.id"), nullable=True)

    orders = relationship("Order", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")
    payment = relationship("Payment", back_populates="customer")