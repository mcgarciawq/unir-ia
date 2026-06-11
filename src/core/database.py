from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ECHO

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=SQLALCHEMY_ECHO, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def get_db():
    """Yield a database session for FastAPI dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
