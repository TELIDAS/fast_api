from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, TEXT, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', default=True)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False,
                          server_default=text("now()"))
    owner_id = Column(Integer,
                      ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False,
                          server_default=text("now()"))


class Auto(Base):
    __tablename__ = 'auto'

    id = Column(Integer, primary_key=True)

    url = Column(String(100), nullable=True)
    title = Column(String(255), nullable=True)
    usd_price = Column(Integer, nullable=True)
    mile_age = Column(Integer, nullable=True)
    username = Column(String(255), nullable=True)
    img_url = Column(TEXT, nullable=True)
    img_total_count = Column(Integer, nullable=True)
    car_number = Column(TEXT, nullable=True)

    created_at = Column(DateTime, default=func.now())
