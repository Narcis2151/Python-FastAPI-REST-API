from typing import Annotated
from fastapi import Depends, Response, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=list[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{post_id}", response_model=schemas.Post)
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.post_id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_item(
    post: schemas.PostBase,
    user_data: Annotated[schemas.TokenData, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    db_post = models.Post(**post.model_dump())
    db_post.user_id = user_data.user_id
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(
    post_id: int,
    new_post: schemas.PostCreate,
    user_data: Annotated[schemas.TokenData, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    post_query = db.query(models.Post).filter(models.Post.post_id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if not post_query.first().user_id == user_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post belongs to a different user",
        )
    post_query.update(new_post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post_query.first())
    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    user_data: Annotated[schemas.TokenData, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    post_query = db.query(models.Post).filter(models.Post.post_id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if not post_query.first().user_id == user_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post belongs to a different user",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
