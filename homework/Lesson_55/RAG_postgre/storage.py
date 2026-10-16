import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql+psycopg2://postgres:{POSTGRES_PASSWORD}@localhost:5432/rag_postgre_demo"

engine = create_engine(DATABASE_URL)
