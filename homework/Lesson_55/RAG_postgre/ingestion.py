import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from google import genai
from sqlalchemy.orm import Session
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from storage import engine
from models import Base, DocumentChunk

sys.stdout.reconfigure(encoding="utf-8")

EMBEDDING_MODEL = "gemini-embedding-001"

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "hotel_info.md"

client = genai.Client()


def ingest():
    Base.metadata.create_all(engine)  # creates the table if it doesn't exist yet

    loader = UnstructuredMarkdownLoader(DATA_PATH)  # load document
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)  # split into chunks
    chunks = splitter.split_documents(docs)

    texts = [chunk.page_content for chunk in chunks]

    result = client.models.embed_content(  # embed chunks
        model=EMBEDDING_MODEL,
        contents=texts,
    )
    embeddings = [item.values for item in result.embeddings]

    with Session(engine) as session:
        session.query(DocumentChunk).delete()  # avoid duplicating rows on re-ingest

        for chunk, embedding in zip(chunks, embeddings):
            document_chunk = DocumentChunk(  # build row
                content=chunk.page_content,
                chunk_metadata=chunk.metadata,
                embedding=embedding,
            )
            session.add(document_chunk)

        session.commit()  # save to db

    print(f"Ingested {len(chunks)} chunks into the database.")


if __name__ == "__main__":
    ingest()
