from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import customers as customer_model
from ..models import sandwiches as sandwich_model
from ..models import payments as payment_model
from ..models import promotions as promotion_model
from ..schemas import orders as schema
from ..schemas import payments as payment_schema
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal
from datetime import datetime, timedelta


def create(db: Session, request):
    try:
        customer = None
        payment = None

        if request.customer_id:
            customer = db.query(customer_model.Customer).filter(customer_model.Customer.id == request.customer_id).first()

            if not customer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

            if customer.default_payment:
                payment = payment_model.Payment(
                    card_info=customer.default_payment.card_info,
                    payment_type=customer.default_payment.payment_type,
                    status=payment_schema.PaymentStatus.SUCCESS
                )
                db.add(payment)
                db.flush()

        new_item = model.Order(
            customer_id=customer.id if customer else None,
            customer_name=customer.customer_name if customer else request.customer_name,
            order_date=request.order_date,
            description=request.description,
            tracking_number=request.tracking_number,
            order_status=schema.OrderStatus.SUCCESS if payment else schema.OrderStatus.PENDING,
            payment_id=payment.id if payment else None,
            price=0.0
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_by_tracking_num(db: Session, tracking_number):
    try:
        order = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()
        if not order:
            raise HTTPException(status_code = 404, detail="Tracking number not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def get_status(db: Session, tracking_number):
    try:
        order = get_by_tracking_num(db, tracking_number)
        if not order:
            raise HTTPException(status_code = 404, detail="Tracking number not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {"tracking_number": tracking_number, "status": order.order_status}


def get_order_by_date(db: Session, start_date, end_date):
    try:
        if isinstance(start_date, str):
            start_obj = datetime.fromisoformat(start_date.replace("Z", "+00:00")).replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)
        else:
            start_obj = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        if isinstance(end_date, str):
            end_obj = datetime.fromisoformat(end_date.replace("Z", "+00:00")).replace(tzinfo=None, hour=23, minute=59, second=59, microsecond=0)
        else:
            end_obj = end_date.replace(hour=23, minute=59, second=59, microsecond=0)
        orders = db.query(model.Order).filter(model.Order.order_date >= start_obj, model.Order.order_date <= end_obj).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return orders


def get_least_ordered(db: Session, date):
    try:
        if isinstance(date, str):
            date_obj = datetime.fromisoformat(date.replace("Z", "+00:00")).replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)
        else:
            date_obj = date.replace(hour=0, minute=0, second=0, microsecond=0)
        orders = db.query(model.Order).filter(model.Order.order_date >= date_obj, model.Order.order_date < date_obj + timedelta(days=1)).all()

        count = {}

        for order in orders:
            for detail in order.order_details:
                if detail.sandwich_id in count:
                    count[detail.sandwich_id] += detail.amount
                else:
                    count[detail.sandwich_id] = detail.amount

        if not count:
            return {"message": "No orders found for this date"}

        least_id = min(count, key=count.get)
        sandwich = db.query(sandwich_model.Sandwich).filter(sandwich_model.Sandwich.id == least_id).first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "sandwich": sandwich,
        "total_ordered": count[least_id]
    }


def get_revenue(db: Session, date):
    try:
        if isinstance(date, str):
            date_obj = datetime.fromisoformat(date.replace("Z", "+00:00")).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            date_obj = date.replace(hour=0, minute=0, second=0, microsecond=0)
        orders = db.query(model.Order).filter(model.Order.order_date >= date_obj, model.Order.order_date < date_obj + timedelta(days=1)).all()
        price = 0
        for order in orders:
            price += order.price
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {"revenue": price}


def apply_promotion(db:Session, item_id, promo_code: str):
    try:
        order = db.query(model.Order).filter(model.Order.id == item_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found!")

        promotion = db.query(promotion_model.Promotion).filter(promotion_model.Promotion.promo_code == promo_code).first()

        if not promotion:
            raise HTTPException(status_code=404, detail="Promotion not found!")

        if promotion.expiration_date < datetime.now():
            raise HTTPException(status_code=400, detail="Promotion expired!")

        if order.discounted_price is not None:
            raise HTTPException(status_code=400, detail="Discount already applied!")

        discount_price = order.price * (Decimal(1) - Decimal(promotion.discount) / Decimal(100))
        order.discounted_price = discount_price

        db.commit()
        db.refresh(order)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def add_payment(db: Session, item_id: int, request):
    try:
        order = db.query(model.Order).filter(model.Order.id == item_id).first()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        if order.payment_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment already exists for this order")

        new_payment = payment_model.Payment(
            card_info=request.card_info,
            payment_type=request.payment_type,
            status=payment_schema.PaymentStatus.SUCCESS
        )
        db.add(new_payment)
        db.flush()
        order.payment_id = new_payment.id
        order.order_status = "Paid"

        db.commit()
        db.refresh(order)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order