import sqlmodel
from sqlmodel import SQLModel, Session, create_engine

# from server.config import DATABASE_URL
from server.config import Config


if Config.DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set")

engine = create_engine(Config.DATABASE_URL)


def init_db():
    print("creating database...")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
