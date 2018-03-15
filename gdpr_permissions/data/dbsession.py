from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import gdpr_permissions.data.classes
import gdpr_permissions.data.pupil
import gdpr_permissions.data.account


class DbSessionFactory:
    factory = None

    @staticmethod
    def global_init(db_file):
        if DbSessionFactory.factory:
            return

        if not db_file or not db_file.strip():
            raise Exception('You must specify a db file!!!')

        conn_str = 'sqlite:///'+db_file
        print(f'Connecting to db file with {conn_str}')

        engine = create_engine(conn_str, connect_args={'check_same_thread': False}, echo=False, poolclass=NullPool)
        Base = declarative_base(bind=engine)
        Base.metadata.create_all(engine)
        DbSessionFactory.factory = sessionmaker(bind=engine)


    @staticmethod
    def create_session():
        return DbSessionFactory.factory()

