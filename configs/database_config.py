from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

engine = create_engine(url="postgresql+psycopg2://postgres:akbarov@localhost/logist_smart", echo=True, pool_size=125, max_overflow=135)

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)
