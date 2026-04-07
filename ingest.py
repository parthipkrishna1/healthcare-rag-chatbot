from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from medquad_loader import load_medquad
from tqdm import tqdm

load_dotenv()

documents = load_medquad("datasets/medquad")

print("Using documents:", len(documents))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print("Total chunks:", len(chunks))

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-chatbot")

# optional clean reset
try:
    index.delete(delete_all=True)
    print("Existing vectors deleted.")
except Exception as e:
    print("No existing vectors to delete.")

vectors = []

for i, chunk in tqdm(enumerate(chunks), total=len(chunks), desc="Embedding chunks"):

    embedding = embeddings.embed_query(chunk.page_content)

    source = chunk.metadata.get("source", "unknown")

    chunk_id = f"{source}_{i}"

    vectors.append({
        "id": chunk_id,
        "values": embedding,
        "metadata": {
            "text": chunk.page_content,
            "source": source,
            "disease": chunk.metadata.get("disease") or "Unknown"
        }
    })

batch_size = 100

for i in tqdm(range(0, len(vectors), batch_size), desc="Uploading vectors"):
    batch = vectors[i:i + batch_size]
    index.upsert(vectors=batch)

print("Vectors inserted:", len(vectors))