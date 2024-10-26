from openai import OpenAI
import os
import asyncio
from fastapi import APIRouter, HTTPException
import os
router = APIRouter()
from database.database import Base, engine

api_key=os.environ.get("OPENAI_API_KEY")

async def heartbeat(api_key):
    try:
        client = OpenAI(api_key=api_key)
        
        # Run the synchronous OpenAI client code in an executor
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": "This is a test"}],
            temperature=0
        )
        return {"status": "API key is valid", "response": response.choices[0].message.content}
    except Exception as e:
        return {"status": "Failed to validate API key", "error": str(e)}
    

@router.get("/heartbeat", tags=["Utilities"])
async def heartbeat_endpoint():
    result = await heartbeat(api_key)
    return(result)

# Endpoint to create or recreate database tables
@router.post("/create-tables", tags=["Utilities"])
async def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        return {"status": "Tables created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating tables: {str(e)}")

# Existing heartbeat endpoint for OpenAI API key validation
async def heartbeat(api_key):
    from openai import OpenAI  # Import here to avoid circular import issues
    try:
        client = OpenAI(api_key=api_key)
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": "This is a test"}],
            temperature=0
        )
        return {"status": "API key is valid", "response": response.choices[0].message.content}
    except Exception as e:
        return {"status": "Failed to validate API key", "error": str(e)}