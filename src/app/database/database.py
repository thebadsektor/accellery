import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database

# Create the directory if it doesn't exist
db_dir = os.path.join(os.path.dirname(__file__), "scaffold")
os.makedirs(db_dir, exist_ok=True)

# Configure the new database URL
DATABASE_URL = f"sqlite:///{db_dir}/test.db"

Base = declarative_base()

# Create the database engine and connect to it
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Create the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the FastAPI database instance
database = Database(DATABASE_URL)