import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from database.database import Base, get_db
from main import app

# Use a separate database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the dependency in the FastAPI app
@pytest.fixture(scope="module")
def db():
    if database_exists(TEST_SQLALCHEMY_DATABASE_URL):
        drop_database(TEST_SQLALCHEMY_DATABASE_URL)
    create_database(TEST_SQLALCHEMY_DATABASE_URL)

    # Create the tables
    Base.metadata.create_all(bind=engine)

    # Provide a session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        drop_database(TEST_SQLALCHEMY_DATABASE_URL)

app.dependency_overrides[get_db] = db
