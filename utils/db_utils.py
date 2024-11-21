from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # 导入 Base
import config

engine = create_engine(config.DATABASE_URI, echo=True)  # echo=True 可以在控制台输出 SQL 语句，方便调试
Session = sessionmaker(bind=engine)


def get_database_session():
    return Session()


def init_db():
    Base.metadata.create_all(engine)
