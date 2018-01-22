from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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

        engine = create_engine(conn_str, echo=False)
        Base = declarative_base(bind=engine)
        Base.metadata.create_all(engine)
        DbSessionFactory.factory = sessionmaker(bind=engine)


    @staticmethod
    def create_session():
        return DbSessionFactory.factory()

