from fastapi import HTTPException
from openai import OpenAIError

from app.core.config import client


EMBEDDING_MODEL = "text-embedding-3-small"


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