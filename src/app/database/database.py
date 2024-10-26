import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set the default database URL for SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./src/app/database/scaffold/test.db")

# Create the directory for SQLite if it doesn't exist
if DATABASE_URL.startswith("sqlite"):
    db_dir = os.path.dirname(DATABASE_URL.split("///")[-1])
    os.makedirs(db_dir, exist_ok=True)

# Initialize the Base class for SQLAlchemy models
Base = declarative_base()

# Create the database engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create all tables defined in models
Base.metadata.create_all(bind=engine)

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
