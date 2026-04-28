from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"


    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    order_date = Column(DATETIME, server_default=str(datetime.now()))
    description = Column(String(300), nullable=True)
    tracking_number = Column(String(100), unique=True)
    order_status = Column(String(50), server_default="Pending")
    price = Column(DECIMAL(10,2))

    order_details = relationship("OrderDetail", back_populates="order")
    customer = relationship("Customer", back_populates="orders")