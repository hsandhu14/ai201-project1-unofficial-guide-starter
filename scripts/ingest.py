from pathlib import Path
import re
import html
import json
import random

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 400
OVERLAP = 50


def clean_text(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_documents():
    documents = []

    for file_path in RAW_DIR.glob("*.txt"):
        raw_text = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "text": clean_text(raw_text)
        })

    return documents


def main():
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{doc['source']}_{i}",
                "source": doc["source"],
                "text": chunk
            })

    output_file = OUT_DIR / "chunks.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Loaded documents: {len(documents)}")
    print(f"Total chunks: {len(all_chunks)}")

    print("\nSample chunks:\n")

    sample = random.sample(all_chunks, min(5, len(all_chunks)))

    for chunk in sample:
        print("=" * 80)
        print(chunk["source"])
        print(chunk["text"])
        print()

if __name__ == "__main__":
    main()