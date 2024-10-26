from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from models.models import Document, Block
from schemas.schemas import Document as DocumentSchema, DocumentCreate
from schemas.schemas import Block as BlockSchema, BlockCreate
from database.database import get_db
from utils.websocket import ConnectionManager
from schemas.schemas import DocumentUpdate  # Ensure this is defined
from schemas.schemas import BlockUpdate  # Ensure this is defined

router = APIRouter(tags=["Documents & Blocks"])
manager = ConnectionManager()

# WebSocket Endpoint
@router.websocket("/ws/{document_id}")
async def websocket_endpoint(websocket: WebSocket, document_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)


# Document Endpoints
@router.get("/documents", response_model=list[DocumentSchema])
def read_documents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents


@router.post("/documents", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    db_document = Document(title=document.title)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


# Block Endpoints
@router.get("/documents/{document_id}/blocks", response_model=list[BlockSchema])
def read_blocks(document_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    blocks = db.query(Block).filter(Block.document_id == document_id).offset(skip).limit(limit).all()
    return blocks


@router.post("/documents/{document_id}/blocks", response_model=BlockSchema, status_code=status.HTTP_201_CREATED)
def create_block(document_id: int, block: BlockCreate, db: Session = Depends(get_db)):
    # Treat parent_id=0 as a top-level block
    parent_id = block.parent_id if block.parent_id and block.parent_id > 0 else None

    db_block = Block(document_id=document_id, parent_id=parent_id, **block.dict(exclude={"parent_id"}))
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block


@router.put("/documents/{document_id}", response_model=DocumentSchema)
def update_document(document_id: int, document: DocumentUpdate, db: Session = Depends(get_db)):
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")

    for key, value in document.dict(exclude_unset=True).items():
        setattr(db_document, key, value)

    db.commit()
    db.refresh(db_document)
    return db_document


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(db_document)
    db.commit()
    return {"message": "Document deleted successfully"}


@router.put("/documents/{document_id}/blocks/{block_id}", response_model=BlockSchema)
def update_block(document_id: int, block_id: int, block: BlockUpdate, db: Session = Depends(get_db)):
    db_block = db.query(Block).filter(Block.document_id == document_id, Block.id == block_id).first()
    if not db_block:
        raise HTTPException(status_code=404, detail="Block not found")

    # Handle parent_id=0
    if block.parent_id == 0:
        block.parent_id = None

    for key, value in block.dict(exclude_unset=True).items():
        setattr(db_block, key, value)

    db.commit()
    db.refresh(db_block)
    return db_block


@router.delete("/documents/{document_id}/blocks/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_block(document_id: int, block_id: int, db: Session = Depends(get_db)):
    db_block = db.query(Block).filter(Block.document_id == document_id, Block.id == block_id).first()
    if not db_block:
        raise HTTPException(status_code=404, detail="Block not found")

    db.delete(db_block)
    db.commit()
    return {"message": "Block deleted successfully"}
