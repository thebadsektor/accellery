from fastapi import APIRouter, HTTPException
from database.database import Base, engine

router = APIRouter()

@router.post("/create-tables", tags=["Utilities"])
async def create_tables():
    try:
        # Log start of table creation
        print("Starting table creation...")
        
        # Create tables in the database
        Base.metadata.create_all(bind=engine)
        
        # Log successful table creation
        print("Tables created successfully.")
        return {"status": "Tables created successfully."}
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating tables: {str(e)}")
