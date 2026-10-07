import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_NAME = "hotel_booking"
DATABASE_URL = f"postgresql+psycopg2://lazosh@/{DB_NAME}"


def create_database_if_missing() -> None:
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    if cursor.fetchone() is None:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
    conn.close()


create_database_if_missing()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
