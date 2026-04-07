from dotenv import load_dotenv
import os
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from sentence_transformers import CrossEncoder

load_dotenv()

# Connect to Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-chatbot")

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Reranker

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Local LLM
llm = OllamaLLM(model="llama3")

def retrieve_context(query):

    query_vector = embeddings.embed_query(query)

    results = index.query(
        vector=query_vector,
        top_k=20,
        include_metadata=True
    )

    pairs = [
        [query, match["metadata"]["text"]]
        for match in results["matches"]
    ]

    scores = reranker.predict(pairs)

    ranked_results = sorted(
        zip(results["matches"], scores),
        key=lambda x: x[1],
        reverse=True
    )

    contexts = []
    sources = []

    for match, score in ranked_results[:3]:
        contexts.append(match["metadata"]["text"])
        sources.append(match["metadata"].get("disease", "Unknown"))

    return "\n".join(contexts), sources


def ask_chatbot(question, history):

    context, sources = retrieve_context(question)

    if not context.strip():
        return "I couldn't find relevant medical information.", []

    chat_history = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in history]
    )

    prompt = f"""
    You are a healthcare assistant.

    Conversation history:
    {chat_history}

    Use ONLY the provided medical context to answer.

    Context:
    {context}

    Question:
    {question}

    If the answer is not present in the context, say you don't know.
    Recommend consulting a healthcare professional when appropriate.
    """


    response = llm.invoke(prompt)

    return response, sources


if __name__ == "__main__":

    history = []

    while True:

        question = input("\nAsk a medical question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        answer, sources = ask_chatbot(question, history)

        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})

        print("\nChatbot:\n", answer)

        print("\nSources:")
        for s in set(sources):
            print("-", s)