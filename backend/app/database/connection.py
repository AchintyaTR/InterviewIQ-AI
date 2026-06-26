import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Fetch DB connection parameters, fallback to sqlite locally for ease of setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./interview_iq.db")

# Use connect_args only for SQLite database sessions
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency provider yielding local database transactions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
