import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

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


@app.get("/")
async def root():
    return {"message": "Welcome Goshojin-sama"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


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
