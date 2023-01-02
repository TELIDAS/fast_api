from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from fast_app.db.models import Base


class Database:
    def __init__(self, connection_url: str = "postgresql://postgres:bjbd672bjhw@localhost/fastapi"):
        # if not database_exists(connection_url):
        #     create_database(connection_url)
        self.engine = create_engine(connection_url)
        # else:
        #     self.engine = create_engine(connection_url)

        self.conn = self.engine.connect()
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

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
