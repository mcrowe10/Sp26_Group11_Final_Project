from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import payments as controller
from ..schemas import payments as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Payments'],
    prefix="/payments"
)


@router.post("/", response_model=schema.Payment)
def create(request: schema.PaymentCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Payment])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{id}", response_model=schema.Payment)
def read_one(id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, id=id)


@router.put("/{id}", response_model=schema.Payment)
def update(id: int, request: schema.PaymentUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, id=id)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, id=id)
