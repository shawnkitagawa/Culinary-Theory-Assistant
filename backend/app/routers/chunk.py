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








