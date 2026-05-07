from fastapi import APIRouter, HTTPException, Request, Query, status
from schema import ChatCreate, ChatCreateResponse, ChatFetchAllResponse, ChatFetchResponse, MessageFetchResponse, MessageCreate, MessageCreateResponse
from sqlalchemy.orm import Session 
from fastapi import Depends
from app.database.base import get_db
from uuid import UUID


router = APIRouter(prefix = "/chats", tags=["chats"])




@router.post("", response_model = ChatCreateResponse,  status_code=status.HTTP_201_CREATED)
def create_chat(create: ChatCreate, db: Session = Depends(get_db)):
    pass 


# handle 404 error 
@router.get("/{chat_id}", response_model = ChatFetchResponse, status_code=status.HTTP_200_OK)
def fetch_chat(chat_id: UUID, db: Session = Depends(get_db)):
    pass 




@router.get("", response_model = ChatFetchAllResponse, status_code=status.HTTP_200_OK)
def fetch_all_chat(offset: int = Query(default = 0 , ge = 0 ), limit: int =  Query(default = 20, ge = 1 , le = 100)):
    pass 



#handle error 404 not found
@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: UUID): 
    pass 



@router.post("/{chat_id}/messages", response_model =MessageCreateResponse, status_code= status.HTTP_201_CREATED)
def create_message(chat_id: UUID, create: MessageCreate, db: Session = Depends(get_db)): 
    pass 

#handle error 404 not found
@router.get("/{chat_id}/messages", response_model = MessageFetchResponse, status_code= status.HTTP_200_OK)
def fetch_all_messages(chat_id: UUID, db: Session = Depends(get_db)): 
    pass 








