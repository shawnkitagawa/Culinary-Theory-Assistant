from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, CheckConstraint, UniqueConstraint, Integer, Enum as SQLEnum, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func , text
from enum import Enum 
from app.database.base import Base
from pgvector.sqlalchemy import Vector

class DocumentStatus(str, Enum): 
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"




class Document(Base): 
    __tablename__ = "documents"

    document_id = Column(UUID(as_uuid=True), primary_key= True, server_default= text("gen_random_uuid()"))
    title = Column(String(255), nullable= False)
    total_page = Column(Integer, nullable= False)
    author = Column(String(255), nullable= True)
    created_at = Column(DateTime(timezone= True), nullable= False, server_default=func.now())
    published_at = Column(DateTime(timezone=True), nullable= True)
    status = Column(SQLEnum(DocumentStatus), nullable= False, server_default=DocumentStatus.PENDING.name)
    file_path = Column(String(255), nullable= False, unique= True ) 




    __table_args__ = (
        UniqueConstraint("title", "author", "file_path" , name = "document_unique"),
    )

class Chunk(Base): 
    __tablename__ = "chunks"

    chunk_id = Column(UUID(as_uuid=True), primary_key= True, server_default= text("gen_random_uuid()"))
    document_id = Column(UUID(as_uuid= True), ForeignKey("documents.document_id", ondelete= "CASCADE"), nullable= False) 
    page_start = Column(Integer, nullable= False)
    page_end = Column(Integer, nullable= False)
    chunk_text = Column(Text, nullable= False)
    embedding = Column(Vector(1536), nullable=False)
    chunk_index = Column(Integer, nullable = False)
    created_at = Column(DateTime(timezone= True), nullable= False, server_default= func.now())


    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index", name = "document_chunk_index_unique"),
    )

Index(
    "chunk_embedding_hnsw_idx", 
    Chunk.embedding, 
    postgresql_using = "hnsw",
    postgresql_ops = {"embedding": "vector_cosine_ops"}
)

