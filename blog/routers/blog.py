from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal, engine, get_db
from ..utils import bcrypt

router = APIRouter(
    prefix='/blogs',
    tags=['blogs']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_a_blog(request: schemas.Blog, db: Session=Depends(get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/', response_model=list[schemas.ShowBlog])
def list_all_blogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/{id}', response_model=schemas.ShowBlog)
def get_a_blog_by_id(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'detail': f'Blog with id {id} is not available'}
        )

    return blog


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_a_blog_by_id(id: int, request: schemas.Blog, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'detail': f'Blog with id {id} not found'}
        )
    
    blog.update(dict(request))
    db.commit()
    return 'updated'


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_a_blog_by_id(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'detail': f'Blog with id {id} not found'}
        )
    
    blog.delete()
    db.commit()
    return 'deleted'
