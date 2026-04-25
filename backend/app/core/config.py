from dotenv import load_dotenv
# from supabase import create_client, Client 
import os 
from pathlib import Path
from openai import OpenAI
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR/ ".env"
load_dotenv(env_path)
DB_PASSWORD = os.getenv("DB_PASSWORD").strip()
MODEL="gpt-4o-mini"


client = OpenAI(api_key= os.getenv("OPENAI_API_KEY").strip())