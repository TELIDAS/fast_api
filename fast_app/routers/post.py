from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import oath2
from ..db import schemas, models
from sqlalchemy.orm import Session
from fast_app.db.database import Database
from ..db.models import Post
from ..db.database import db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post], )
async def get_posts(current_user: int = Depends(oath2.get_current_user)):
    print(str(current_user))
    """ all posts """
    # posts = db.query(models.Post).all()

    """all posts by owner_id """
    posts = db.get_users_list_data(id=current_user.id)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
async def create_post(post: schemas.PostCreate,
                      current_user: int = Depends(oath2.get_current_user)):
    data = Post(
        title=post.title,
        description=post.description,
        published=post.published,
        owner_id=current_user.id,

    )
    db.save_objects(objects=data)

    return data


@router.get("/{id}", response_model=schemas.Post)
async def get_post_detail(id: int,
                          current_user: schemas.UserLogin = Depends(oath2.get_current_user)):
    post = db.get_data(table=models.Post, id=id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return post


@router.delete("/{id}")
async def delete_post(id: int,
                      current_user: int = Depends(oath2.get_current_user)
                      ):
    post = db.get_users_data(id=id)
    users_post = db.delete_users_data(table=models.Post, id=id)
    if users_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        users_post = db.delete_users_data(table=models.Post, id=id)
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
