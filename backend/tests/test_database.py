import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # ✅ Use declarative_base from sqlalchemy.orm

# Use localhost when testing outside Docker
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5434/sensors_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # ✅ Corrected import
