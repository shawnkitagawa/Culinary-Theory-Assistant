from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.database.db import DocumentStatus


class StrictnessLevel(str, Enum):
    strict = "strict"
    balanced = "balanced"
    creative = "creative"
    recipe = "recipe"


class ResponseLanguage(str, Enum):
    auto = "auto"
    english = "english"
    japanese = "japanese"


# -------------------------
# Answer Schemas
# -------------------------

class AnswerCreate(BaseModel):
    chat_id: UUID | None = None
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=10)
    strictness: StrictnessLevel = StrictnessLevel.balanced
    response_language: ResponseLanguage = ResponseLanguage.auto


class MessageSourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | int
    document_title: str
    page_start: int
    page_end: int
    similarity: float
    chunk_text: str


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: datetime
    sources: list[MessageSourceResponse] = []


class AnswerCreateResponse(BaseModel):
    chat_id: UUID
    user_message: MessageResponse
    assistant_message: MessageResponse
    sources: list[MessageSourceResponse]


# -------------------------
# Chat Schemas
# -------------------------

class ChatCreate(BaseModel):
    question: str | None = None


class ChatCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    created_at: datetime
    self: str


class ChatFetchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    created_at: datetime
    messages: list[MessageResponse]
    self: str


class ChatFetchAllResponse(BaseModel):
    entries: list[ChatCreateResponse]
    next: str | None = None


# -------------------------
# Message Schemas
# -------------------------

class MessageCreate(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(..., min_length=1)


class MessageCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    chat_id: UUID
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: datetime
    self: str
    chat: str


class MessageFetchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    chat_id: UUID
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: datetime
    sources: list[MessageSourceResponse] = []
    self: str


# -------------------------
# Document Schemas
# -------------------------

class DocumentCreate(BaseModel):
    title: str = Field(..., max_length=255)
    total_page: int = Field(..., ge=1)
    author: str | None = Field(default=None, max_length=255)
    published_at: datetime | None = None
    file_path: str


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: UUID
    title: str
    total_page: int
    author: str | None = None
    created_at: datetime
    published_at: datetime | None = None
    status: DocumentStatus
    file_path: str
    self: str


class DocumentFetchAllResponse(BaseModel):
    entries: list[DocumentResponse]
    next: str | None = None


# -------------------------
# Chunk Schemas
# -------------------------

class ChunkSearchCreate(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=10)
    max_distance: float | None = None