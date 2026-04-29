from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..schemas import payments as payment_schema
from ..dependencies.database import engine, get_db
from datetime import datetime

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.get("/{tracking_number}", response_model=schema.Order)
def track(tracking_number: str, db: Session = Depends(get_db)):
    return controller.get_by_tracking_num(db, tracking_number=tracking_number)


@router.get("/status/{tracking_number}")
def status(tracking_number: str, db: Session = Depends(get_db)):
    return controller.get_status(db, tracking_number=tracking_number)


@router.get("/{date}", response_model=list[schema.Order])
def by_date(start: datetime, end: datetime, db:Session = Depends(get_db)):
    return controller.get_order_by_date(db, start_date=start, end_date=end)


@router.get("/least_ordered/{date}")
def least_ordered(date: datetime, db: Session = Depends(get_db)):
    return controller.get_least_ordered(db, date=date)


@router.get("/revenue/{date}")
def revenue(date: datetime, db: Session = Depends(get_db)):
    return controller.get_revenue(db, date=date)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.put("/promotion/{item_id}", response_model=schema.Order)
def promotion(item_id: int, promo_code: str,  db: Session = Depends(get_db)):
    return controller.apply_promotion(db=db, item_id=item_id, promo_code=promo_code)


@router.post("/payment/{item_id}", response_model=schema.Order)
def payment(item_id: int, request: payment_schema.PaymentCreate, db: Session = Depends(get_db)):
    return controller.add_payment(db=db, item_id=item_id, request=request)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
