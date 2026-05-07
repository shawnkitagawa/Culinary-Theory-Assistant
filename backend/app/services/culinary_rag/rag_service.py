from sqlalchemy.orm import Session

from app.core.config import client, MODEL
from schema import RecipeCreate
from app.services.culinary_rag.retrieval import get_closest_chunks
from app.services.culinary_rag.context_builder import get_context_text
from app.services.culinary_rag.prompts import system_prompt, user_prompt, fail_statement
from app.services.culinary_rag.strictness import get_strict_config
from app.services.culinary_rag.source_formatter import format_sources




def generate_rag_answer(recipe_request: RecipeCreate, db: Session) -> dict:
    strictness = recipe_request.strictness.value
    language = recipe_request.response_language.value
    question = recipe_request.question

    config = get_strict_config(strictness)

    results = get_closest_chunks(recipe_request=recipe_request, db=db)

    
    results = [
    (chunk, document_title, distance_score)
    for chunk, document_title, distance_score in results
    if distance_score < config["max_distance"]
]
        
    if not results:
        answer = fail_statement(strictness)

        return {
            "answer": answer,
            "sources": [],
        }

    context_text = get_context_text(results)

    system = system_prompt(strictness=strictness, language=language)
    user = user_prompt(question=question, context_text=context_text)

    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=config["temperature"],
    )

    return {
        "answer": response.output_text,
        "sources": format_sources(results),
    }