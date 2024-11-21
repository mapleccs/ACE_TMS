from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import config


def get_database_session():
    engine = create_engine(config.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def close_session(session):
    session.close()
