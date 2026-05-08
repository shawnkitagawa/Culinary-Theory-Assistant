from fastapi import APIRouter, HTTPException, Request, Query, status, Response
from fastapi.responses import JSONResponse
from schema import ChatCreate, ChatCreateResponse, ChatFetchAllResponse, ChatFetchResponse, MessageFetchResponse, MessageCreate, MessageCreateResponse
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import Depends
from app.database.db import Chat, Message
from app.database.base import get_db
from uuid import UUID
from app.core.config import client, MODEL, BASE_URL
from app.services.culinary_rag.prompts import TITLE_SYSTEM_PROMPT
from openai import(
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    PermissionDeniedError,
    RateLimitError,
    InternalServerError,
)
from app.services.culinary_rag.utils import fallback_title

router = APIRouter(prefix = "/chats", tags=["chats"])

@router.post("", response_model = ChatCreateResponse,  status_code=status.HTTP_201_CREATED)
def create_chat(create: ChatCreate, db: Session = Depends(get_db)):

    try: 
        question = create.question
        response = client.responses.create(
            model = MODEL, 
            input = [
                {

                
                "role": "system", 
                "content" : TITLE_SYSTEM_PROMPT, 
                },
                {
                    "role":"user", 
                    "content": f"Create a title for this question: {create.question}"
                }
            ]
        )

        title = response.output_text.strip()

        if not title:
            title = fallback_title(question)
    
    except(RateLimitError, APIConnectionError, InternalServerError): 
        title = fallback_title(question)

    except(AuthenticationError, PermissionDeniedError): 

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content = {"Error": "OpenAI configuration error while generating chat title"}
        )
    
    except BadRequestError: 

        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {"Error": "OpenAI request error while generating chat title"} 
        )
    
    except Exception: 
        title =  fallback_title(question)
    
    try:
        new_chat = Chat(
            title=title
        )

        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)

    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "Error": "Database constraint violation"
            },
        )
    except SQLAlchemyError: 
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content = {
                "Error": "Database error occurred"
            }
        )

    return {
        "id": str(new_chat.id),
        "title": new_chat.title,
        "created_at": new_chat.created_at.isoformat().replace("+00:00", "Z"),
        "self": f"{BASE_URL}/chats/{new_chat.id}",
    }


# handle 404 error 
@router.get("/{chat_id}", response_model = ChatFetchResponse, status_code=status.HTTP_200_OK)
def fetch_chat(chat_id: UUID, db: Session = Depends(get_db)):
    
    chat = db.query(Chat).filter(Chat.id == chat_id).first()


    if chat is None: 
        return JSONResponse(status_code= 404, content= {"Error": "No chat with this chat_id exists"})
    
    return {
        "id": chat.id, 
        "title": chat.title, 
        "created_at": chat.created_at.isoformat().replace("+00:00", "Z"), 
        "messages": [
            {
                "id": message.id, 
                "chat_id": message.chat_id, 
                "role": message.role, 
                "content": message.content, 
                "created_at": message.created_at, 
                "sources": message.sources if hasattr(message, "sources") else [], 
                "self": f"{BASE_URL}/messages/{message.id}"
            }
            for message in chat.messages
        ],
        "self": f"{BASE_URL}/chats/{chat.id}"
    }



@router.get("", response_model = ChatFetchAllResponse, status_code=status.HTTP_200_OK)
def fetch_all_chat(offset: int = Query(default = 0 , ge = 0 ), limit: int =  Query(default = 20, ge = 1 , le = 100), db: Session = Depends(get_db)):

    chats = db.query(Chat).offset(offset).limit(limit).all()
    
    return {
        "entries": [
            {

            
            "id": chat.id, 
            "title": chat.title, 
            "created_at": chat.created_at.isoformat().replace("+00:00", "Z"), 
            "self": f"{BASE_URL}/chats/{chat.id}"
            }
            for chat in chats
        ],
        "next": f"{BASE_URL}/chats?offset={offset + limit}&limit={limit}"
    }
    


#handle error 404 not found
@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: UUID, db: Session = Depends(get_db)): 

    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    if chat is None: 
        return JSONResponse(status_code=404, content = {"Error":"No chat with this chat_id exists" })
    
    db.delete(chat) 
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.post("/{chat_id}/messages", response_model =MessageCreateResponse, status_code= status.HTTP_201_CREATED)
def create_message(chat_id: UUID, create: MessageCreate, db: Session = Depends(get_db)): 

    try: 
        chat = db.query(Chat).filter(Chat.id == chat_id).first()

        if chat is None: 
            return JSONResponse(status_code=404, content = {"Error": "No chat with this chat_id exists"})

        new_message = Message(
            chat_id = chat_id, 
            role = create.role, 
            content = create.content
        )

        db.add(new_message) 
        db.commit()
        db.refresh(new_message) 

        return {
            "id": new_message.id,
            "chat_id": chat_id, 
            "role": new_message.role, 
            "content": new_message.content, 
            "created_at": new_message.created_at, 
            "self": f"{BASE_URL}/messages/{new_message.id}",
            "chat": f"{BASE_URL}/chats/{chat_id}"
        }
    except IntegrityError:
        db.rollback()
        return JSONResponse(status_code=409, content = {"Error": "Database constraint violation"})

#handle error 404 not found
@router.get("/{chat_id}/messages", response_model = list[MessageFetchResponse], status_code= status.HTTP_200_OK)
def fetch_all_messages(chat_id: UUID, db: Session = Depends(get_db)): 
    
    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    if chat is None: 
        return JSONResponse(status_code=404, content = {"Error": "No chat with this chat_id exists"})
    
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()

    return [
    {
        "id": message.id, 
        "chat_id": message.chat_id, 
        "role": message.role, 
        "content": message.content, 
        "created_at": message.created_at, 
        "sources": [{
            "id": source.id, 
            "document_title": source.document_title, 
            "page_start": source.page_start, 
            "page_end": source.page_end, 
            "similarity": source.similarity,
            "chunk_text": source.chunk_text, 
        }
        for source in message.sources
        ],
        "self": f"{BASE_URL}/messages/{message.id}"
    }
    for message in messages
]
    
    










