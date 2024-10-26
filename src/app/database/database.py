import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set the database URL for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

# Initialize the Base class for SQLAlchemy models
Base = declarative_base()

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create all tables defined in models (this will be triggered via an endpoint)
# Base.metadata.create_all(bind=engine)

# Create the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the FastAPI database instance for async operations
database = Database(DATABASE_URL)

# Dependency to get a database session (for sync operations)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
