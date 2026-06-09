from pathlib import Path
import json

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path("data/processed/chunks.json")
CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "uwt_professor_reviews"

MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_vector_store(chunks):
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Reset collection so rerunning the script does not duplicate chunks.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": i
        }
        for i, chunk in enumerate(chunks)
    ]

    embeddings = model.encode(texts).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return collection, model


def retrieve(query, collection, model, top_k=TOP_K):
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return results


def print_results(query, results):
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances), start=1):
        print(f"\nResult {i}")
        print(f"Source: {metadata['source']}")
        print(f"Chunk index: {metadata['chunk_index']}")
        print(f"Distance: {distance:.4f}")
        print("Text:")
        print(doc)


def main():
    chunks = load_chunks()
    print(f"Loaded chunks: {len(chunks)}")

    collection, model = build_vector_store(chunks)
    print("Vector store built successfully.")

    test_queries = [
        "Which professor is helpful during office hours",
        "Which professor is a tough grader",
        "Which professor uses projects in class"
    ]

    for query in test_queries:
        results = retrieve(query, collection, model)
        print_results(query, results)


if __name__ == "__main__":
    main()