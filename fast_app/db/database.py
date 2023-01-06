from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import delete

from fast_app.db import models
from fast_app.db.models import Base


class Database:
    def __init__(self, connection_url: str = "postgresql://postgres:bjbd672bjhw@localhost/fastapi"):
        self.engine = create_engine(connection_url)
        self.conn = self.engine.connect()
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def get_data(self, table, id: int):
        data = self.session.query(table).filter_by(id=id).first()
        return data

    def get_users_list_data(self, id):
        users_data = self.session.query(models.Post).filter(models.Post.owner_id == id).all()
        return users_data

    def get_users_data(self, id):
        users_data = self.session.query(models.Post).filter(models.Post.id == id).first()
        return users_data

    def delete_users_data(self, table, id):
        # delete(models.Post).where(models.Post.id == id)
        self.session.query(models.Post).delete(models.Post.id == id)
        self.commit()

    def save_objects(self, objects):

        self.session.add(objects)
        self.commit()

    def commit(self):
        try:
            self.session.commit()
        except IntegrityError as e:
            print(e)
            self.session.rollback()
        except Exception as e:
            print(e)
            self.session.rollback()


db = Database()
