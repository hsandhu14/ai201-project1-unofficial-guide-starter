from pathlib import Path
import json
import os

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

CHUNKS_FILE = Path("data/processed/chunks.json")
CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "uwt_professor_reviews"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5
GROQ_MODEL = "llama-3.3-70b-versatile"


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_collection():
    chunks = load_chunks()
    embedder = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        collection = client.create_collection(COLLECTION_NAME)

        texts = [chunk["text"] for chunk in chunks]
        ids = [chunk["id"] for chunk in chunks]
        metadatas = [
            {
                "source": chunk["source"],
                "chunk_index": i
            }
            for i, chunk in enumerate(chunks)
        ]

        embeddings = embedder.encode(texts).tolist()

        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    return collection, embedder


collection, embedder = get_collection()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve(query, top_k=TOP_K):
    query_embedding = embedder.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []

    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "distance": distance
        })

    return chunks


def build_context(chunks):
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['source']}, chunk {chunk['chunk_index']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def ask(question):
    retrieved_chunks = retrieve(question)
    context = build_context(retrieved_chunks)

    sources = sorted(set(chunk["source"] for chunk in retrieved_chunks))

    system_prompt = """
You are a grounded question-answering assistant for a student-built RAG system.

Rules:
1. Answer using ONLY the provided context.
2. Do not use outside knowledge.
3. If the context does not contain enough information, say: "I don't have enough information on that."
4. Be specific and mention professor names only when supported by the context.
5. Do not invent facts, courses, ratings, or opinions.
"""

    user_prompt = f"""
Context:
{context}

Question:
{question}

Answer using only the context above.
"""

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources,
        "chunks": retrieved_chunks
    }


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question, or type 'quit': ")

        if question.lower() == "quit":
            break

        result = ask(question)

        print("\nAnswer:")
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print(f"- {source}")