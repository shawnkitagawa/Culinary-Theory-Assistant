from fastapi import HTTPException
from openai import OpenAIError

from app.core.config import client, EMBEDDING_MODEL


def text_to_vector(text: str) -> list[float]:
    text = text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty",
        )

    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
        )

        return response.data[0].embedding

    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="AI embedding service error",
        )
    
def fallback_title(question: str) -> str: 
    title = question.strip()

    if not title: 
        return "Untitled Conversation"
    
    return title[:60].rstrip()
    
