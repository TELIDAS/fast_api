from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from .. import utils
from ..db import schemas, models
from fast_app.db.database import Database
from ..db.models import User
from ..db.database import db
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    data = User(
        email=user.email,
        password=user.password,
    )
    db.save_objects(data)
    return data


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int):
    user = db.get_data(table=User, id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user
