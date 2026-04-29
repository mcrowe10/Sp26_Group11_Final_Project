from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import promotion as model


def create_promotion(db: Session, request):
    promotion = model.Promotion(**request.dict())
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return promotion

def update_promotion(db: Session, promotion_id, request):
    promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id)

    if not promotion.first():
        raise HTTPException(status_code=404, detail="Promotion not found")

    promotion.update(request.dict())
    db.commit()
    return promotion

def delete_promotion(db: Session, promotion_id):
    promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id)

    if not promotion.first():
        raise HTTPException(status_code=404, detail="Promotion not found")

    db.delete(promotion)
    db.commit()


def read_all(db: Session):
    try:
        promotion = db.query(model.Promotion).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return promotion


def read_one(db: Session, promotion_id: int):
    try:
        promotion = db.query(model.Promotion).filter(
            model.Promotion.id == promotion_id
        ).first()

        if not promotion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promotion not found"
            )

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    return promotion