import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity

# Windows encoding fix
sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")
load_dotenv()

EMBEDDING_MODEL = "gemini-embedding-001"

# Resolve data path
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "hotel_info.md"

# Load document
loader = UnstructuredMarkdownLoader(DATA_PATH)
docs = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)
chunks = splitter.split_documents(docs)

print(f"Number of chunks: {len(chunks)}")

texts = [chunk.page_content for chunk in chunks]

client = genai.Client()

# Embed all chunks
result = client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=texts,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
)

embeddings = [item.values for item in result.embeddings]

print(f"Number of embeddings: {len(embeddings)}")
print(f"Embedding dimensions: {len(embeddings[0])}")

# Get user question
question = input("Enter your question: ")

# Embed the question
query_result = client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=question,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
)
embedding_query = query_result.embeddings[0].values

# Compute cosine similarity
similarity_scores = cosine_similarity([embedding_query], embeddings)[0]

# Rank chunks by score
results = sorted(zip(chunks, similarity_scores), key=lambda x: x[1], reverse=True)

# Print top 3 matches
print("\nTop 3 most relevant chunks:")
for chunk, score in results[:3]:
    print("========================================")
    print(f"Score: {score}")
    print(f"Data: {chunk.page_content}")
