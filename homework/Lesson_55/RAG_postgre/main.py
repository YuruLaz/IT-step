import sys

from dotenv import load_dotenv

load_dotenv()

from google import genai
from sqlalchemy import select
from sqlalchemy.orm import Session
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from storage import engine
from models import DocumentChunk

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

EMBEDDING_MODEL = "gemini-embedding-001"

client = genai.Client()


def retrieve_documents(question: str, top_k: int = 3):
    query_result = client.models.embed_content(  # embed question
        model=EMBEDDING_MODEL,
        contents=question,
    )
    query_embedding = query_result.embeddings[0].values

    query = (
        select(DocumentChunk)
        .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))  # cosine distance
        .limit(top_k)  # top 3
    )

    with Session(engine) as session:
        return session.execute(query).scalars().all()  # run query


def format_documents(documents):  # build context
    return "\n\n".join(chunk.content for chunk in documents)


prompt = ChatPromptTemplate.from_messages(  # grounding prompt
    [
        (
            "system",
            "You are a helpful assistant. Answer the question based only "
            "on the following context.\n"
            "Don't add anything else, just answer the question.\n"
            "If you don't know the answer, just say that you don't know.",
        ),
        ("human", "Context: {context}\n\nQuestion: {question}"),
    ]
)

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

chain = prompt | llm | StrOutputParser()  # LCEL chain


def answer_question(question: str):  # full RAG step
    documents = retrieve_documents(question)
    context = format_documents(documents)

    return chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )


if __name__ == "__main__":
    while True:  # interactive loop
        question = input("Enter your question (or 'exit' to quit): ")

        if question.lower() == "exit":
            break

        response = answer_question(question)

        print("=" * 20)
        print(response)
