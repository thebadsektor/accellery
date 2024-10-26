# src/app/tests/test_documents.py

import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base, get_db

# Set up a separate test database (replace with your test database URL)
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a TestClient instance
client = TestClient(app)

# Create tables before running tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Test cases
def test_create_document():
    response = client.post("/api/v1/documents", json={"title": "Test Document"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Document"

def test_get_documents():
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_block():
    # Ensure a document exists
    doc_response = client.post("//api/v1documents", json={"title": "Document with Blocks"})
    document_id = doc_response.json()["id"]

    # Create a block under the document
    response = client.post(
        f"/api/v1/documents/{document_id}/blocks",
        json={"type": "Title", "content": "Block Content", "order": 1, "parent_id": None}
    )
    assert response.status_code == 201
    assert response.json()["type"] == "Title"

def test_get_blocks():
    # Ensure a document exists
    doc_response = client.post("/api/v1/documents", json={"title": "Document for Block Retrieval"})
    document_id = doc_response.json()["id"]

    # Create a block under the document
    client.post(
        f"/api/v1/documents/{document_id}/blocks",
        json={"type": "Header", "content": "Header Content", "order": 1, "parent_id": None}
    )

    # Retrieve blocks
    response = client.get(f"/api/v1/documents/{document_id}/blocks")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_document():
    # Create a document
    response = client.post("/api/v1/documents", json={"title": "Document to Update"})
    document_id = response.json()["id"]

    # Update the document
    response = client.put(f"/api/v1/documents/{document_id}", json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_document():
    # Create a document
    response = client.post("/api/v1/documents", json={"title": "Document to Delete"})
    document_id = response.json()["id"]

    # Delete the document
    response = client.delete(f"/api/v1/documents/{document_id}")
    assert response.status_code == 204

def test_update_block():
    # Ensure a document exists
    doc_response = client.post("/api/v1/documents", json={"title": "Document for Block Update"})
    document_id = doc_response.json()["id"]

    # Create a block under the document
    block_response = client.post(
        f"/api/v1/documents/{document_id}/blocks",
        json={"type": "Header", "content": "Initial Content", "order": 1, "parent_id": None}
    )
    block_id = block_response.json()["id"]

    # Update the block
    response = client.put(
        f"/api/v1/documents/{document_id}/blocks/{block_id}",
        json={"content": "Updated Content"}
    )
    assert response.status_code == 200
    assert response.json()["content"] == "Updated Content"

def test_delete_block():
    # Ensure a document exists
    doc_response = client.post("/api/v1/documents", json={"title": "Document for Block Deletion"})
    document_id = doc_response.json()["id"]

    # Create a block under the document
    block_response = client.post(
        f"/api/v1/documents/{document_id}/blocks",
        json={"type": "Paragraph", "content": "Content to Delete", "order": 1, "parent_id": None}
    )
    block_id = block_response.json()["id"]

    # Delete the block
    response = client.delete(f"/api/v1/documents/{document_id}/blocks/{block_id}")
    assert response.status_code == 204
