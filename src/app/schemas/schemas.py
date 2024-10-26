from pydantic import BaseModel
from typing import List, Dict

class ProductSchema(BaseModel):
    id: str
    name: str
    handle: str
    description: str
    category: str
    categories: List[str]
    tags: List[str]
    featuredImageId: str
    images: List[dict]
    priceTaxExcl: float
    priceTaxIncl: float
    taxRate: float
    comparedPrice: float
    quantity: float
    sku: str
    width: str
    height: str
    depth: str
    weight: str
    extraShippingFee: float
    active: bool
    title: str
    slug: str
    duration: int
    totalSteps: int
    updatedAt: str
    featured: bool
    progress: List[dict]
    steps: List[dict]
    summaries: List[dict]

class SumdocSchema(BaseModel):
    id: str
    name: str
    handle: str
    description: str
    category: str
    categories: List[str]
    tags: List[str]
    featuredImageId: str
    images: List[dict]
    priceTaxExcl: float
    priceTaxIncl: float
    taxRate: float
    comparedPrice: float
    quantity: float
    sku: str
    width: str
    height: str
    depth: str
    weight: str
    extraShippingFee: float
    active: bool
    title: str
    slug: str
    duration: int
    totalSteps: int
    updatedAt: str
    featured: bool
    progress: List[dict]
    steps: List[dict]
    summaries: List[dict]


class SummarySchema(BaseModel):
    id : str
    doc_id: str
    model: str
    content: str
    updatedAt: str
    createdAt: str