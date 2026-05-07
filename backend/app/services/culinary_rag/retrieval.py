from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.db import Document, Chunk
from schema import RecipeCreate
from app.services.culinary_rag.utils import text_to_vector
from app.services.culinary_rag.translation import translate_to_english

def get_closest_chunks(recipe_request:RecipeCreate, db: Session) -> list[tuple[Chunk, str, float]]: 
    message = recipe_request.question.strip()
        
    if recipe_request.response_language.value == "japanese":
        message = translate_to_english(message)

    if not message:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    vector = text_to_vector(message)
    distance = Chunk.embedding.cosine_distance(vector)

    results = (
        db.query(
            Chunk,
            Document.title.label("document_title"),
            distance.label("distance")
        )
        .join(Document, Chunk.document_id == Document.document_id)
        .order_by(distance)
        .limit(recipe_request.top_k)
        .all()
    )

    return results
