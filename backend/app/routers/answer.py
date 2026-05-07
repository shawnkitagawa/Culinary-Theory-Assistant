from fastapi import APIRouter, Depends, HTTPException, Request, status
from openai import OpenAIError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import traceback
from app.database.db import Chat
from app.core.config import limiter
from app.database.base import get_db
from schema import AnswerCreate, AnswerCreateResponse
from app.services.culinary_rag.rag_service import generate_rag_answer

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
                    status_code=404,
                    detail="No chat with this chat_id exists",
                )
    
        return generate_rag_answer(recipe_request=recipe_request, db=db)

    except HTTPException:
        raise

    except OpenAIError as e:
        print("OPENAI ERROR TYPE:", type(e).__name__)
        print("OPENAI ERROR REPR:", repr(e))
        print("OPENAI ERROR MESSAGE:", str(e))
        print("OPENAI ERROR CAUSE:", repr(e.__cause__) if e.__cause__ else "None")
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI service error while generating the answer",
        )

    except SQLAlchemyError as e:
        print("Database Error:", e)
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while searching documents",
        )

    except Exception as e:
        print("Unexpected error:", e)
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The answer could not be generated",
        )