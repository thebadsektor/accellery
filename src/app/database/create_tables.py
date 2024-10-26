# create_tables.py

from models.models import Base, Document, Block
from database.database import engine
from sqlalchemy import inspect

def create_all_tables():
    try:
        print(f"Creating tables in: {engine.url}")
        Base.metadata.create_all(bind=engine)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables found after creation: {tables}")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")

if __name__ == "__main__":
    create_all_tables()
