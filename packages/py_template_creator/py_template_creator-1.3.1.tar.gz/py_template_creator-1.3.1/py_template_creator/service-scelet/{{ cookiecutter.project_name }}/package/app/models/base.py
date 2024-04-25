import logging
import os

from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

logger = logging.getLogger(__name__)

DB_URL = "postgresql+psycopg://{}:{}@{}:{}/{}".format(
    os.getenv("POSTGRES_USER"),
    os.getenv("POSTGRES_PASSWORD"),
    os.getenv("POSTGRES_HOST"),
    os.getenv("POSTGRES_PORT"),
    os.getenv("POSTGRES_DB"),
)
logger.info(f"Connecting with conn string {DB_URL}")


engine = create_engine(DB_URL, pool_pre_ping=True, poolclass=NullPool)
Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


def get_db_session():
    try:
        db = Session()
        yield db
    finally:
        db.close()
