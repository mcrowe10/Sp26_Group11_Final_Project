from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"


    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    order_date = Column(DATETIME, default=lambda: datetime.now())
    description = Column(String(300), nullable=True)
    tracking_number = Column(String(100), unique=True)
    order_status = Column(String(50))
    price = Column(DECIMAL(10,2))
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    discounted_price = Column(DECIMAL(10,2), nullable=True)

    order_details = relationship("OrderDetail", back_populates="order")
    customer = relationship("Customer", back_populates="orders")
    payment = relationship("Payment", back_populates="orders")