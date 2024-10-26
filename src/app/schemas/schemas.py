from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

# Sample Schema
# class ProductSchema(BaseModel):
#     id: str
#     name: str
#     handle: str
#     description: str
#     category: str
#     categories: List[str]
#     tags: List[str]
#     featuredImageId: str
#     images: List[dict]
#     priceTaxExcl: float
#     priceTaxIncl: float
#     taxRate: float
#     comparedPrice: float
#     quantity: float
#     sku: str
#     width: str
#     height: str
#     depth: str
#     weight: str
#     extraShippingFee: float
#     active: bool
#     title: str
#     slug: str
#     duration: int
#     totalSteps: int
#     updatedAt: str
#     featured: bool
#     progress: List[dict]
#     steps: List[dict]
#     summaries: List[dict]


# Document Schemas
class DocumentBase(BaseModel):
    title: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Block Schemas
class BlockBase(BaseModel):
    type: str
    content: Optional[str] = None
    order: int
    parent_id: Optional[int] = None

class BlockCreate(BlockBase):
    pass

class Block(BlockBase):
    id: int
    document_id: int

    class Config:
        orm_mode = True

class DocumentUpdate(BaseModel):
    title: Optional[str] = None

    class Config:
        orm_mode = True

class BlockUpdate(BaseModel):
    type: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True