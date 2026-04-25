from fastapi import FastAPI, APIRouter, HTTPException, Request
import re
from openai import OpenAI, OpenAIError
import os 
from app.core.config import client, MODEL
from sqlalchemy.orm import Session 
from fastapi import Depends
from app.database.base import get_db
from pathlib import Path 
from app.database.db import Document, Chunk
from sqlalchemy.exc import SQLAlchemyError
from app.services.culinary_rag.utils import text_to_vector
from app.database.db import Document, Chunk
from sqlalchemy.orm import Session 
from fastapi import Depends
from schema import RecipeCreate
import traceback
from app.core.config import limiter


router = APIRouter(prefix = "/answer", tags =["answer"])



@router.post("/")
@limiter.limit("5/10minutes")
def generate_recipe(recipe_request: RecipeCreate, request: Request, db: Session = Depends(get_db)):
    try:
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

        results = [row for row in results if row.distance < 0.50]

        if not results:
            fallback_by_mode = {
                "strict": (
                    "I could not find enough directly relevant source material to answer this in strict mode.\n\n"
                    "Try asking a question that is more directly covered by the culinary sources."
                ),
                "balanced": (
                    "I could not find strong enough source material for this question in the current culinary library.\n\n"
                    "Try rephrasing the question or asking about a related cooking principle, ingredient, or technique."
                ),
                "creative": (
                    "I could not find enough relevant source material to make a reliable theory-based application.\n\n"
                    "Try asking about a broader culinary principle, such as texture, flavor balance, freezing, fermentation, sauces, or cooking methods."
                ),
                "recipe": (
                    "I could not find enough relevant source material to create a source-backed recipe recommendation.\n\n"
                    "Try asking about a recipe idea connected to the current culinary sources, such as ice cream, gelato, fruit, dairy, sauces, fermentation, or cooking technique."
                )
            }

            return {
                "answer": fallback_by_mode.get(
                    recipe_request.strictness.value,
                    "I could not find enough relevant source material for this question."
                ),
                "sources": []
            }
            

        contexts = []

        for chunk, document_title, distance_score in results:
            contexts.append(
            f"[Source: {document_title}, Pages {chunk.page_start}-{chunk.page_end}]\n"
            f"{chunk.chunk_text}"
)

        context_text = "\n\n---\n\n".join(contexts)


        STRICTNESS_CONFIG = {
        "strict": {
            "temperature": 0.1,
            "max_distance": 0.42,
            "instruction": (
                "Answer only with facts that are directly stated in the provided context. "
                "Do not add outside knowledge, examples, assumptions, or creative suggestions. "
                "If the context does not clearly answer the question, say: "
                "'I don't know based on the provided material.' "
                "Keep the answer concise. "
                "When possible, cite the exact source label and page range from the context."
            )
        },

        "balanced": {
            "temperature": 0.3,
            "max_distance": 0.55,
            "instruction": (
                "Answer using the provided context as the source of truth. "
                "Explain the culinary theory, principles, causes, effects, and practical meaning. "
                "If the context partially answers the question, clearly say what is supported and what is not directly covered. "
                "You may give practical advice only when it logically follows from the retrieved context. "
                "Do not invent specific ingredients, recipes, or techniques that are not supported by the context. "
                "Use simple, clear English."
            )
        },

        "creative": {
            "temperature": 0.55,
            "max_distance": 0.70,
            "instruction": (
                "Use the provided context as the foundation. "
                "If the context contains relevant culinary principles, mechanisms, techniques, or examples, do not stop at 'I don't know.' "
                "First explain what the sources directly support. "
                "Then add a clearly labeled section called 'Theory-based application' for reasonable extensions. "
                "The theory-based application must be connected to the retrieved context. "
                "Do not pretend creative applications are directly stated in the source. "
                "When suggesting ingredients or techniques, prefer examples from the context. "
                "If the exact ingredient is not in the context, speak in categories and principles rather than making unsupported source claims. "
                "Focus on useful culinary reasoning, tradeoffs, and practical implications."
            )
        },

        "recipe": {
            "temperature": 0.65,
            "max_distance": 0.75,
            "instruction": (
                "Generate a helpful recipe-style recommendation using the retrieved context as the culinary foundation. "
                "Recipe mode should be practical and useful, not overly defensive. "
                "If the retrieved context does not mention the user's exact ingredient, but it contains related culinary theory, similar ingredients, "
                "fruit preparations, dairy principles, freezing principles, sugar balance, texture control, flavor balance, or technique examples, "
                "use those principles to make a careful recommendation. "
                "Clearly separate direct source support from creative application. "
                "Use these sections when appropriate: "
                "'Short answer', 'Supported by the sources', 'Creative recipe application', 'Basic method', and 'Why it works'. "
                "You may suggest reasonable spice combinations, flavor pairings, ingredient amounts, and methods as creative applications. "
                "Do not claim those suggestions are directly from the sources unless the context directly states them. "
                "If the exact topic is not directly covered, say: 'The sources do not directly mention this exact combination, but they provide related principles.' "
                "Only say 'I don't know based on the provided material' if the retrieved context is completely unrelated to the user's question."
            )
        }
    }

        mode_extra_rule = (
            "For recipe mode, be useful and practical. You may add clearly labeled creative recipe applications, "
            "including reasonable ingredients, spice pairings, methods, and amounts, as long as the culinary reasoning is connected to the retrieved context. "
            "Never claim a creative suggestion is directly from the source unless the context directly states it."
            if recipe_request.strictness.value == "recipe"
            else (
                "For creative mode, you may include clearly labeled theory-based applications when the context is relevant but incomplete. "
                "For strict and balanced modes, do not invent ingredients, techniques, or facts not supported by the context."
                if recipe_request.strictness.value == "creative"
                else "Do not invent ingredients, techniques, or facts not supported by the context."
            )
        )

        language_instruction = (
            "Answer in natural Japanese."
            if recipe_request.response_language.value == "japanese"
            else "Answer in clear, natural English."
        )

        system_prompt = f"""
        You are a professional culinary theory assistant.

        Your job is to help the user understand cooking through source-backed culinary reasoning.
        Use the retrieved context as the foundation for your answer.

        Core rules:
        - Be helpful, clear, and practical.
        - Focus on culinary theory, principles, mechanisms, causes, effects, and tradeoffs.
        - Do not pretend the sources say something they do not say.
        - If the exact ingredient, recipe, or technique is not directly mentioned, say that clearly.
        - If the retrieved context is still related, use it to explain a careful theory-based or recipe-based application.
        - Clearly separate direct source support from creative application.
        - {mode_extra_rule}
        - When useful, cite the exact source label from the context, including page range.
        - Only cite sources that directly support the point being made.
        - Do not over-apologize.
        - Do not end with generic phrases like "feel free to ask."
        - Make the answer feel confident, professional, and useful.

        Strictness mode: {recipe_request.strictness.value}

        Mode-specific instruction:
        {STRICTNESS_CONFIG[recipe_request.strictness.value]["instruction"]}

        If the retrieved context only describes a specific version of the user's request,
        clearly say that. For example:
        "The provided context describes a chicken cutlet method using chicken breast."

        Do not present a specific recipe as the only or universal answer unless the context supports that.

        {language_instruction}

        Citation rule:
        When citing sources, copy the exact source label from the context.
        Example citation format:
        [Source: Book Title, Pages 10-12]
        """

        user_prompt = f"""
        Retrieved context:
        {context_text}

        User question:
        {message}

        Answer the user according to the selected strictness mode.
        """


        response = client.responses.create(
            model=MODEL,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature= STRICTNESS_CONFIG[recipe_request.strictness.value]["temperature"]
        )

        answer = response.output_text

        return {
            "answer": answer ,
            "sources": [
                {
                    "chunk_id": str(chunk.chunk_id),
                    "document_title": document_title,
                    "page_start": chunk.page_start,
                    "page_end": chunk.page_end,
                    "distance": distance_score,
                    "similarity": 1 - distance_score,
                }
                for chunk, document_title, distance_score in results
            ]
        }

    except HTTPException:
        raise

    except OpenAIError as e:

        print("OPENAI ERROR TYPE:", type(e).__name__)
        print("OPENAI ERROR REPR:", repr(e))
        print("OPENAI ERROR MESSAGE:", str(e))
        print("OPENAI ERROR CAUSE:", repr(e.__cause__) if e.__cause__ else "None")
        traceback.print_exc()
        raise HTTPException(
            status_code=502,
            detail="AI service error while generating the answer"
        )

    except SQLAlchemyError as e:
        print("Database Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Database error while searching documents"
        )

    except Exception as e:
        print("Unexpected error:", e)
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while answering the question"
        )
    

def translate_to_english(text:str) -> str: 
    response = client.responses.create(
        model = MODEL, 
        input = [
            {
                "role": "system", 
                "content": "Translate the user's text into natural English. Return only the translation."
            },
            {
            "role": "user",
            "content": text
        }
        ],
        temperature = 0.1
    )
    return response.output_text.strip()


def translate_to_japanese(text:str) -> str: 
    response = client.responses.create(
        model = MODEL, 
        input = [
            {
                "role": "system", 
                "content": "Translate the user's text into natural Japanese. Return only the translation."
            },
            {
            "role": "user",
            "content": text
        }
        ],
        temperature = 0.1
    )
    return response.output_text.strip()