import psycopg2
from typing import List
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)
fast_app = FastAPI()

try:
    connection = psycopg2.connect(host='localhost',
                                  port=5432,
                                  database='fastapi',
                                  user='postgres',
                                  password='postgres',
                                  cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print('Database connection successful')
except Exception as error:
    print("Failed Connection to db")
    print(f'Error: {error}')


@fast_app.get("/")
async def root():
    return {"message": "Welcome Goshojin-sama"}


@fast_app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@fast_app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@fast_app.post("/posts", status_code=status.HTTP_201_CREATED,
               response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(
        **post.dict()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@fast_app.get("/posts/{id}", response_model=schemas.Post)
async def get_post_detail(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return post


@fast_app.delete("/posts/{id}")
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@fast_app.put("/posts/{id}", response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post


@fast_app.post("/users",
               status_code=status.HTTP_201_CREATED,
               response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(
        **user.dict()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@fast_app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user

# @fast_app.get("/sql/posts")
# async def sql_get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"data": posts}

# @fast_app.post('/sql/posts', status_code=status.HTTP_201_CREATED)
# def sql_create_post(post: schemas.PostBase):
#     cursor.execute("""INSERT INTO posts (title, description, published) VALUES (%s, %s, %s) RETURNING * """,
#                    (post.title, post.description, post.published))
#     new_post = cursor.fetchone()
#     connection.commit()
#     return {"data": new_post}


# @fast_app.get("/sql/posts/{id}")
# def sql_get_post_detail(id: str):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id), )
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} was not found")
#     return {"detail": post}

# @fast_app.delete("/sql/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def sql_delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id), )
#     deleted_post = cursor.fetchone()
#     connection.commit()
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id: {id} does not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @fast_app.put("/sql/posts/{id}")
# def sql_update_post(id: int, post: schemas.PostBase):
#     cursor.execute("""UPDATE posts SET title = %s, description = %s, published = %s WHERE id = %s RETURNING *""",
#                    (post.title, post.description, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     connection.commit()
#     if updated_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id: {id} does not exist")
#     return {"data": updated_post}
