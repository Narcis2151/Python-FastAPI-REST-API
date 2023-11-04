from fastapi import Depends, Response, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db, engine, Base

post_router = APIRouter()


@post_router.get("/posts", response_model=list[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@post_router.get("/posts/{post_id}", response_model=schemas.Post)
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@post_router.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post
)
async def create_item(post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@post_router.put("/posts/{post_id}", response_model=schemas.Post)
async def update_post(
    post_id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    post_query.update(new_post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post_query.first())
    return post_query.first()


@post_router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)