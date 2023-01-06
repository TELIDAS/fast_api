from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import oath2
from ..db import schemas, models
from sqlalchemy.orm import Session
from fast_app.db.database import Database

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post], )
async def get_posts(db: Session = Depends(Database),
                    current_user: int = Depends(oath2.get_current_user)):
    print(str(current_user))
    """ all posts """
    # posts = db.query(models.Post).all()

    """all posts by owner_id """
    posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id
    ).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
async def create_post(post: schemas.PostCreate,
                      db: Session = Depends(Database),
                      current_user: int = Depends(oath2.get_current_user)):
    new_post = models.Post(
        owner_id=current_user.id,
        **post.dict()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
async def get_post_detail(id: int,
                          db: Session = Depends(Database),
                          current_user: schemas.UserLogin = Depends(oath2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return post


@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(Database),
                      current_user: int = Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostBase,
                      db: Session = Depends(Database),
                      current_user: int = Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are now allowed to do such action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post
