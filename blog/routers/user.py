from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal, engine, get_db
from ..utils import bcrypt

router = APIRouter(
    prefix='/users',
    tags=['Users'] 
)


@router.post(
    '/', 
    response_model=schemas.ShowUser, 
    status_code=status.HTTP_201_CREATED
)
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.ShowUser)
def get_a_user_by_id(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'detail': f'User with id {id} is not available'}
        )

    return user