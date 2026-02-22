import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

class Base(DeclarativeBase): 
    pass

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://eitaa_user:eitaa_pass@localhost:5432/eitaa"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)