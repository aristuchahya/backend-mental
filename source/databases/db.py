from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os import getenv


DATABASE_URL = getenv("DATABASE_URL", "postgresql+psycopg2://postgres:namikaze43@127.0.0.1:5432/mental_health_disease2")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()
