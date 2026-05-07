from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, CheckConstraint, UniqueConstraint, Integer, Enum as SQLEnum, Text, Index, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func , text
from enum import Enum 
from app.database.base import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship

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


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid = True), primary_key=True, server_default = text("gen_random_uuid()"))
    title = Column(Text, nullable=False, default="New Chat")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default = text("gen_random_uuid()"))
    chat_id = Column(
        UUID,
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    chat = relationship("Chat", back_populates="messages")

    sources = relationship(
        "MessageSource",
        back_populates="message",
        cascade="all, delete-orphan",
    )


class MessageSource(Base):
    __tablename__ = "message_sources"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(
        UUID,
        ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_title = Column(Text, nullable=False)
    page_start = Column(Integer, nullable=True)
    page_end = Column(Integer, nullable=True)
    similarity = Column(Float, nullable=True)
    chunk_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    message = relationship("Message", back_populates="sources")



Index(
    "chunk_embedding_hnsw_idx", 
    Chunk.embedding, 
    postgresql_using = "hnsw",
    postgresql_ops = {"embedding": "vector_cosine_ops"}
)

