from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine
from .utils import bcrypt

app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
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


@app.get('/blog', response_model=list[schemas.ShowBlog], tags=['blogs'])
def list_all_blogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['blogs'])
def get_a_blog_by_id(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'detail': f'Blog with id {id} is not available'}
        )

    return blog


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
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


@app.delete('/blogs/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
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


@app.post(
    '/users',
    response_model=schemas.ShowUser,
    status_code=status.HTTP_201_CREATED,
    tags=['users']
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


@app.get('/users/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_a_user_by_id(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'detail': f'User with id {id} is not available'}
        )

    return user