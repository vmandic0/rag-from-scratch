import argparse
import hashlib
from pathlib import Path

import chromadb

from chunking import chunk_document
from config import CHUNK_OVERLAP, CHUNK_WORDS, COLLECTION, DB_DIR, DOCS_DIR
from ollama_client import embed_documents


def _file_hash(text):
    """Računa SHA-256 otisak sadržaja dokumenta i parametara chunkovanja."""
    payload = f"{text}|{CHUNK_WORDS}|{CHUNK_OVERLAP}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _document_is_unchanged(collection, filename, file_hash):
    """Proverava da li je dokument već obrađen i nepromenjen."""
    result = collection.get(
        where={"source": filename},
        include=["metadatas"],
    )
    metadatas = result.get("metadatas") or []
    return bool(metadatas) and all(
        metadata and metadata.get("file_hash") == file_hash
        for metadata in metadatas
    )


def _ingest_file(collection, path):
    """Obrađuje jedan Markdown dokument i upisuje njegove chunkove."""
    text = path.read_text(encoding="utf-8")
    file_hash = _file_hash(text)

    if _document_is_unchanged(collection, path.name, file_hash):
        print(f"Preskačem nepromenjen dokument: {path.name}")
        return 0

    collection.delete(where={"source": path.name})
    chunks = chunk_document(text, CHUNK_WORDS, CHUNK_OVERLAP)

    texts = [chunk["text"] for chunk in chunks]
    ids = [f"{path.name}::{index}" for index in range(len(chunks))]
    metadatas = [
        {
            "source": path.name,
            "section": chunk["section"],
            "file_hash": file_hash,
        }
        for chunk in chunks
    ]
    vectors = []
    for batch_start in range(0, len(chunks), 16):
        batch_texts = texts[batch_start:batch_start + 16]
        vectors.extend(embed_documents(batch_texts))

    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=texts,
        metadatas=metadatas,
    )

    print(f"Obrađen dokument: {path.name} ({len(chunks)} chunkova)")
    return len(chunks)


def main():
    """Učitava dokumente i upisuje njihove embedding-e u Chroma bazu."""
    parser = argparse.ArgumentParser(description="Učitavanje dokumenata u Chroma bazu.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Obriši postojeću kolekciju pre učitavanja.",
    )
    args = parser.parse_args()

    client = chromadb.PersistentClient(path=DB_DIR)
    if args.reset:
        try:
            client.delete_collection(COLLECTION)
        except chromadb.errors.NotFoundError:
            pass
    collection = client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    for path in sorted(Path(DOCS_DIR).glob("*.md")):
        _ingest_file(collection, path)

    current_files = {path.name for path in Path(DOCS_DIR).glob("*.md")}
    metadatas = collection.get(include=["metadatas"]).get("metadatas") or []
    sources = {
        metadata["source"]
        for metadata in metadatas
        if metadata and "source" in metadata
    }
    for name in sources - current_files:
        collection.delete(where={"source": name})
        print(f"Uklonjen dokument: {name} (fajl više ne postoji)")

    print(f"Ukupno chunkova u kolekciji: {collection.count()}")


if __name__ == "__main__":
    main()
