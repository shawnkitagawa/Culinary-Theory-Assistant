from pydantic import BaseModel, Field
from app.database.db import DocumentStatus
from enum import Enum 

class StrictnessLevel(str, Enum):
    strict = "strict"
    balanced = "balanced"
    creative = "creative"
    recipe = "recipe"

class ResponseLanguage(str, Enum):
    auto = "auto"
    english = "english"
    japanese = "japanese"


class RecipeCreate(BaseModel):
    question: str
    top_k: int = Field(default=5, ge=1, le=10)
    strictness: StrictnessLevel = StrictnessLevel.balanced
    response_language: ResponseLanguage = ResponseLanguage.auto,