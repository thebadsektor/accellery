from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database.database import Base
from datetime import datetime

Base = declarative_base()

# Sample Model
# class Product(Base):
#     __tablename__ = "products"
#     id = Column(String, primary_key=True, index=True)
#     name = Column(String)
#     handle = Column(String)
#     description = Column(String)
#     category = Column(String)
#     categories = Column(JSON)
#     tags = Column(JSON)
#     featuredImageId = Column(String)
#     images = Column(JSON)
#     priceTaxExcl = Column(Float)
#     priceTaxIncl = Column(Float)
#     taxRate = Column(Float)
#     comparedPrice = Column(Float)
#     quantity = Column(Float)
#     sku = Column(String)
#     width = Column(String)
#     height = Column(String)
#     depth = Column(String)
#     weight = Column(String)
#     extraShippingFee = Column(Float)
#     active = Column(Boolean)
#     title = Column(String)
#     slug = Column(String)
#     duration = Column(Integer)
#     totalSteps = Column(Integer)
#     updatedAt = Column(String)
#     featured = Column(Boolean)
#     progress = Column(JSON)
#     steps = Column(JSON)
#     summaries = Column(JSON)

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    blocks = relationship("Block", back_populates="document", cascade="all, delete-orphan")

class Block(Base):
    __tablename__ = 'blocks'

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    type = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey('blocks.id'), nullable=True)  # Allowing parent_id to be nullable

    document = relationship("Document", back_populates="blocks")
    children = relationship("Block", backref="parent", remote_side=[id])