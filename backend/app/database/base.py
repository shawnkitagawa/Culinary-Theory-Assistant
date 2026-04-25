from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
import os 
from dotenv import load_dotenv
from pathlib import Path
from app.core.config import DB_PASSWORD

from urllib.parse import quote_plus

password = quote_plus(DB_PASSWORD)

DATABASE_URL=f"postgresql+psycopg2://postgres:{password}@db.wxcgowndnovamwekgjil.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL) 

SessionLocal = sessionmaker(

    autocommit=False, 

    autoflush=False,
    bind= engine 
)


Base = declarative_base()

def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
