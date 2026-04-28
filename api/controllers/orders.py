from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import customers as customer_model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta


def create(db: Session, request):
    try:
        customer = None

        if request.customer_id:
            customer = db.query(customer_model.Customer).filter(
                customer_model.Customer.id == request.customer_id).first()

            if not customer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )

        new_item = model.Order(
            customer_name=customer.customer_name if customer else request.customer_name,        order_date=request.order_date,
            description=request.description,
            tracking_number=request.tracking_number,
            order_status=request.order_status,
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
        order = db.query(model.Order).filter(model.Order.order_date >= start_date, model.Order.order_date <= end_date).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def get_least_ordered(db: Session, date):
    try:
        if isinstance(date, str):
            date_obj = datetime.fromisoformat(date.replace("Z", "+00:00")).replace(hour=0, minute=0, second=0, microsecond=0)
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
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "sandwich_id": least_id,
        "total_ordered": count[least_id]
    }