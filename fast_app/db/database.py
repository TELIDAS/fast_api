from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_app.db import models
from fast_app.db.models import Base
from ..config import DB_URI


class Database:
    def __init__(self, connection_url: str = DB_URI):
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
        data = self.session.query(table).get(id)
        if data is None:
            return None
        else:
            self.session.delete(data)
            self.commit()

    def update_post(self, table, id: int, query: dict):
        self.session.query(table).filter(models.Post.id == id).update(query)
        self.commit()

    def save_objects(self, objects):
        exists = self.session.query(models.Auto).filter_by(url=objects.url).first() is not None
        print(exists)
        if exists:
            pass
        else:
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
