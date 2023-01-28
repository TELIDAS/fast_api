from sqlalchemy.orm import Session

from .db import database, schemas, models
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .db.database import db
from fast_app.config import SECRET_KEY, ALGORITHM

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    encoding = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoding.update({"exp": expire})
    encoded_token = jwt.encode(encoding, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_token


def verify_access_token(token: str,
                        credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate ",
        headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.session.query(models.User).filter(models.User.id == token.id).first()
    return user
