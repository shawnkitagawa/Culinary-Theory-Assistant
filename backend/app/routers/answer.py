from fastapi import APIRouter, Depends, HTTPException, Request, status
from openai import (
    APIConnectionError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    OpenAIError,
    PermissionDeniedError,
    RateLimitError,
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
import traceback

from app.core.config import client, limiter, MODEL
from app.database.base import get_db
from app.database.db import Chat, Message
from app.services.culinary_rag.rag_service import generate_rag_answer
from app.services.culinary_rag.utils import fallback_title
from schema import AnswerCreate, AnswerCreateResponse


router = APIRouter(prefix="/answer", tags=["answer"])

@router.post(
    "",
    response_model=AnswerCreateResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/10minutes")
def generate_recipe(
    request: Request,
    recipe_request: AnswerCreate,
    db: Session = Depends(get_db),
):
    try:
        if recipe_request.chat_id:
            chat = db.query(Chat).filter(Chat.id == recipe_request.chat_id).first()

            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No chat with this chat_id exists",
                )

        else:
            question = recipe_request.question

            try:
                title_response = client.responses.create(
                    model=MODEL,
                    input=[
                        {
                            "role": "system",
                            "content": TITLE_SYSTEM_PROMPT,
                        },
                        {
                            "role": "user",
                            "content": f"Create a short title for this question: {question}",
                        },
                    ],
                )

                title = title_response.output_text.strip() or fallback_title(question)

            except (RateLimitError, APIConnectionError, InternalServerError):
                title = fallback_title(question)

            except (AuthenticationError, PermissionDeniedError):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="OpenAI configuration error while generating chat title",
                )

            except BadRequestError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="OpenAI request error while generating chat title",
                )

            except Exception:
                title = fallback_title(question)

            chat = Chat(title=title)
            db.add(chat)
            db.flush()
            db.refresh(chat)

            recipe_request = recipe_request.model_copy(
                update={"chat_id": chat.id}
            )

        rag_response = generate_rag_answer(
            recipe_request=recipe_request,
            db=db,
        )

        db.commit()

        return {
            "chat_id": chat.id,
            "answer": rag_response["answer"],
            "sources": rag_response["sources"],
        }

    except HTTPException:
        db.rollback()
        raise

    except OpenAIError as e:
        db.rollback()
        print("OPENAI ERROR TYPE:", type(e).__name__)
        print("OPENAI ERROR REPR:", repr(e))
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI service error while generating the answer",
        )

    except IntegrityError as e:
        db.rollback()
        print("Integrity Error:", e)
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database constraint violation",
        )

    except SQLAlchemyError as e:
        db.rollback()
        print("Database Error:", e)
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while generating the answer",
        )

    except Exception as e:
        db.rollback()
        print("Unexpected error:", e)
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The answer could not be generated",
        )