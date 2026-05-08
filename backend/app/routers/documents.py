from fastapi import APIRouter, HTTPException, status, Query, Response
from fastapi.responses import JSONResponse
import re
import os 
from sqlalchemy.orm import Session 
from fastapi import Depends
from app.database.base import get_db
from pathlib import Path 
from app.database.db import Document, Chunk
from sqlalchemy.exc import IntegrityError
from app.services.culinary_rag.utils import text_to_vector
from schema import DocumentCreate, DocumentFetchAllResponse,DocumentResponse, DocumentStatus
from app.core.config import BASE_URL
from uuid import UUID 


FOLDER_PATH = Path(r"C:\Users\seank\Desktop\PROJECT_FREE\Q-A-StudyAssistant\raw_text")

router = APIRouter(prefix = "/ingest", tags =["ingest"])


def clean_text(text: str) -> str:
    # replace newlines and multiple spaces
    text = text.replace("\x00", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_raw_text(text: str) -> str:
    # Keep newlines/page markers
    return text.replace("\x00", "")


def chunk_text_with_pages(text: str, chunk_size: int = 300, overlap: int = 50) -> list[dict]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    lines = text.splitlines()
    current_page = 0

    word_buffer = []
    page_buffer = []
    chunks = []
    index = 0 

    for line in lines:
        line = line.strip()
        if not line:
            continue

        page_match = re.match(r"--- Page (\d+) ---", line)
        if page_match:
            current_page = int(page_match.group(1))
            continue

        if line == "[No text found]":
            continue

        line = re.sub(r"[ \t]+", " ", line)
        words = line.split()


        for word in words:
            word_buffer.append(word)
            page_buffer.append(current_page)

            if len(word_buffer) == chunk_size:
                chunk_content = clean_text(" ".join(word_buffer))
                index += 1 

                chunks.append({
                    "content": chunk_content,
                    "page_start": min(page_buffer) if page_buffer else 0,
                    "page_end": max(page_buffer) if page_buffer else 0,
                    "embedding": text_to_vector(chunk_content),
                    "chunk_index": index
                })

                word_buffer = word_buffer[chunk_size - overlap:]
                page_buffer = page_buffer[chunk_size - overlap:]

    if word_buffer:
        chunk_content = clean_text(" ".join(word_buffer))
        index += 1 
        chunks.append({
            "content": chunk_content,
            "page_start": min(page_buffer) if page_buffer else 0,
            "page_end": max(page_buffer) if page_buffer else 0,
            "embedding": text_to_vector(chunk_content),
            "chunk_index": index
        })

    return chunks


def createDocument(text: str, file_name: str, file_path: str): 
    match = re.match(r"---\s*Page\s+(\d+)\s*---", text)
    page_matches = re.findall(r"---\s*Page\s+(\d+)\s*---", text)
    total_page = max(map(int, page_matches)) if page_matches else 0
    title = re.sub(r"\.txt$", "", file_name)
    author = None 
    published_at = None

    return {
        "title": title, 
        "total_page": total_page,
        "author": author, 
        "published_at": published_at, 
        "file_path": file_path
    }



    #Logical ERROR!!
@router.post("/", response_model = DocumentResponse, status_code=status.HTTP_201_CREATED)
def ingest_document(db: Session = Depends(get_db)): 
      # 1. create document row
    try: 

        for filename in os.listdir(FOLDER_PATH):
            if not filename.endswith(".txt"):
                continue

            file_path = os.path.join(FOLDER_PATH, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            text = clean_raw_text(text)

            document = createDocument(text, filename, file_path)

            new_document = Document(
                title =  document["title"], 
                total_page = document["total_page"], 
                author = document["author"], 
                published_at =  document["published_at"], 
                file_path = document["file_path"], 
            )

            db.add(new_document)
            db.flush()

            chunks = chunk_text_with_pages(text)

            print("TEXT LENGTH:", len(text))
            print("CHUNKS CREATED:", len(chunks))

            if len(chunks) == 0:
                print("WARNING: No chunks created for", filename)

            for chunk in chunks: 
             
                new_chunk = Chunk(
                    document_id = new_document.document_id, 
                    page_start = chunk["page_start"],
                    page_end = chunk["page_end"],
                    chunk_text = chunk["content"], 
                    embedding = chunk["embedding"], 
                    chunk_index = chunk["chunk_index"], 
                )
                db.add(new_chunk)
       


            db.commit()
            db.refresh(new_document)

        return {
            "document_id": new_document.document_id, 
            "title": new_document.title, 
            "total_page": new_document.total_page, 
            "author": new_document.author, 
            "created_at": new_document.created_at, 
            "published_at": new_document.published_at, 
            "status": new_document.status, 
            "file_path": new_document.file_path, 
            "self": f"{BASE_URL}/documents/{new_document.document_id}"

        }
        
    except IntegrityError as e: 
        db.rollback()
        print("IntegrityError:", e)
        return JSONResponse(status_code=409, content = {"Error": "A document with this file_path already exists"})
    
    except Exception as e: 
        db.rollback()
        print("ERROR TYPE", type(e))
        print("ERROR MESSAGE", str(e))
        raise HTTPException(status_code= 500, detail = "Internal Server error during ingestion")



@router.get("/{document_id}", response_model = DocumentResponse, status_code=status.HTTP_200_OK)
def fetch_document(document_id: UUID, db: Session = Depends(get_db)): 

    document = db.query(Document).filter(Document.document_id == document_id).first()

    if document is None: 
        return JSONResponse(status_code=404, content = {"Error": "No document with this document_id exists"})

    
    return {
        "document_id": document.document_id, 
        "title": document.title, 
        "total_page": document.total_page, 
        "author": document.author, 
        "created_at": document.created_at, 
        "published_at": document.published_at, 
        "status": document.status, 
        "file_path": "uploads/the_professional_chef.pdf", 
        "self": "https://culinary-rag-api.example.com/documents/1fcd7a5a-9a5c-4c02-bf3f-81a29a0a1111" 

    }



@router.get("/", response_model= DocumentFetchAllResponse, status_code=status.HTTP_200_OK)
def fetch_all_documents(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
): 
    documents = db.query(Document).offset(offset).limit(limit).all()

    return {
        "entries": [
            {
                "document_id": document.document_id, 
                "title": document.title, 
                "total_page": document.total_page, 
                "author": document.author, 
                "created_at": document.created_at, 
                "published_at": document.published_at, 
                "status": document.status, 
                "file_path": document.file_path, 
                "self": f"{BASE_URL}/documents/{document.document_id}" 
            }
            for document in documents
        ],
        "next": f"{BASE_URL}/documents?offset={offset + limit}&limit={limit}"
    }




@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: UUID, db: Session = Depends(get_db)): 

    document = db.query(Document).filter(Document.document_id == document_id).first()


    if document is None: 
        return JSONResponse(status_code=404, content = {"Error": "No document with this document_id exists" })
    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)







