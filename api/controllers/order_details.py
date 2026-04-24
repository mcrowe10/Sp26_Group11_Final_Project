from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status, Response, Depends
from ..models import order_details as model
from ..models import sandwiches as sandwich_model
from ..models import recipes as recipe_model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.OrderDetail(
        order_id=request.order_id,
        sandwich_id=request.sandwich_id,
        amount=request.amount
    )

    try:
        sandwich = db.query(sandwich_model.Sandwich).options(
            joinedload(sandwich_model.Sandwich.recipe)
            .joinedload(recipe_model.Recipe.resource)
        ).filter(
            sandwich_model.Sandwich.id == request.sandwich_id
        ).first()

        if not sandwich:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!"
            )

        if not sandwich.recipe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No recipe defined for this sandwich!"
            )

        resource_updates = []

        for recipe in sandwich.recipe:
            resource = recipe.resource
            required_amount = recipe.amount * request.amount

            if not resource:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resource {recipe.resource_id} not found!"
                )

            if resource.amount < required_amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough {resource.name} in stock"
                )

            resource_updates.append((resource, required_amount))

        for resource, required_amount in resource_updates:
            resource.amount -= required_amount

        new_item = model.OrderDetail(
            order_id=request.order_id,
            sandwich_id=request.sandwich_id,
            amount=request.amount
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
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()
