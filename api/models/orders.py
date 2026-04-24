from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300), nullable=True, server_default="")
    tracking_number = Column(String(100), unique=True, nullable=False)
    order_status = Column(String(50), nullable=False, server_default="pending")
    price = Column(DECIMAL(10,2), nullable=False, server_default='0.0')

    order_details = relationship("OrderDetail", back_populates="order")
    customer = relationship("Customer", back_populates="orders")
