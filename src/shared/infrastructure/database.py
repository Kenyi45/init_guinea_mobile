from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import StaticPool
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Configure engine based on database type
if DATABASE_URL and "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}
    poolclass = StaticPool
else:
    connect_args = {}
    poolclass = None

engine = create_engine(
    DATABASE_URL,
    poolclass=poolclass,
    connect_args=connect_args,
    echo=os.getenv("DEBUG", "False").lower() == "true"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables."""
    Base.metadata.create_all(bind=engine) 