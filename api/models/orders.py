from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    tracking_number = Column(Integer)
    order_status = Column(String(50))
    payment_status = Column(String(50), ForeignKey("payments.status"))
    price = Column(DECIMAL(10,2))

    order_details = relationship("OrderDetail", back_populates="order")
    customers = relationship("Customer", back_populates="order")
    payments = relationship("Payment", back_populates="order")