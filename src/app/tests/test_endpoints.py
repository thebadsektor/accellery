import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.database import Base, get_db
from app.models.models import Document, Block

# Setup a temporary SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the override to the app
app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

# Setup and teardown the database before and after each test
@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Test cases for Document endpoints
def test_create_document():
    response = client.post("/api/v1/documents", json={"title": "Test Document"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Document"

def test_read_documents():
    client.post("/api/v1/documents", json={"title": "Test Document"})
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Document"

def test_update_document():
    client.post("/api/v1/documents", json={"title": "Old Title"})
    response = client.put("/api/v1/documents/1", json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_document():
    client.post("/api/v1/documents", json={"title": "Test Document"})
    response = client.delete("/api/v1/documents/1")
    assert response.status_code == 204
    response = client.get("/api/v1/documents")
    assert len(response.json()) == 0

# Test cases for Block endpoints
def test_create_block():
    client.post("/api/v1/documents", json={"title": "Test Document"})
    response = client.post("/api/v1/documents/1/blocks", json={"type": "text", "content": "Test Content", "order": 1})
    assert response.status_code == 201
    assert response.json()["content"] == "Test Content"

def test_read_blocks():
    client.post("/api/v1/documents", json={"title": "Test Document"})
    client.post("/api/v1/documents/1/blocks", json={"type": "text", "content": "Test Content", "order": 1})
    response = client.get("/api/v1/documents/1/blocks")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["content"] == "Test Content"

def test_update_block():
    client.post("/api/v1/documents", json={"title": "Test Document"})
    client.post("/api/v1/documents/1/blocks", json={"type": "text", "content": "Old Content", "order": 1})
    response = client.put("/api/v1/documents/1/blocks/1", json={"content": "New Content"})
    assert response.status_code == 200
    assert response.json()["content"] == "New Content"

def test_delete_block():
    client.post("/api/v1/documents", json={"title": "Test Document"})
    client.post("/api/v1/documents/1/blocks", json={"type": "text", "content": "Test Content", "order": 1})
    response = client.delete("/api/v1/documents/1/blocks/1")
    assert response.status_code == 204
    response = client.get("/api/v1/documents/1/blocks")
    assert len(response.json()) == 0
