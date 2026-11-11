import argparse

import chromadb

from config import COLLECTION, DB_DIR, MAX_DISTANCE, TOP_K
from ollama_client import chat, embed_query


NO_ANSWER = "I could not find this in the provided documents."
SYSTEM_PROMPT = (
    "You answer questions using ONLY the CONTEXT in the user's message. "
    "If the CONTEXT contains the answer, state it in one to three full sentences "
    "and include the exact values, numbers or names from the CONTEXT. "
    "Only if the CONTEXT clearly does not contain the answer, "
    "reply with exactly this sentence and nothing else: "
    f'"{NO_ANSWER}"'
)


def get_collection():
    """Otvara Chroma kolekciju."""
    client = chromadb.PersistentClient(path=DB_DIR)
    return client.get_collection(COLLECTION)


def retrieve(collection, question, k=TOP_K):
    """Pretražuje kolekciju i vraća pronađene odlomke."""
    vector = embed_query(question)
    result = collection.query(query_embeddings=[vector], n_results=k)
    return [
        {
            "text": text,
            "source": metadata["source"],
            "section": metadata["section"],
            "distance": distance,
        }
        for text, metadata, distance in zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        )
    ]


def build_prompt(question, hits):
    """Gradi upit sa kontekstom pronađenih odlomaka."""
    context = "\n\n".join(
        f"[{hit['source']}]\n{hit['text']}"
        for hit in hits
    )
    return f"CONTEXT:\n{context}\n\nQUESTION: {question}"


def answer(collection, question, k=TOP_K, max_distance=MAX_DISTANCE):
    """Pretražuje dokumente i generiše odgovor."""
    hits = retrieve(collection, question, k)
    used = [hit for hit in hits if hit["distance"] <= max_distance]
    if not used:
        return {
            "answer": NO_ANSWER,
            "retrieved": hits,
            "used": used,
            "prompt_tokens": None,
        }

    text, prompt_tokens, _ = chat(
        SYSTEM_PROMPT,
        build_prompt(question, used),
    )
    text = text.strip()
    if NO_ANSWER.rstrip(".") in text:
        text = NO_ANSWER
    else:
        sources = sorted({h["source"] for h in used})
        text = text + " [" + ", ".join(sources) + "]"
    return {
        "answer": text,
        "retrieved": hits,
        "used": used,
        "prompt_tokens": prompt_tokens,
    }


def show(question, result, debug=False):
    """Ispisuje pitanje, odgovor i pronađene odlomke."""
    print(f"Q: {question}")
    print(f"A: {result['answer']}")
    print("Retrieved chunks (distance, source, section):")
    for hit in result["retrieved"]:
        label = "(used)" if hit in result["used"] else "(below threshold)"
        print(
            f"{hit['distance']:.3f}, {hit['source']} "
            f"[{hit['section']}] {label}"
        )
        if debug:
            print(f"  {hit['text']}")
    if debug and result["prompt_tokens"] is not None:
        print(f"Prompt tokens: {result['prompt_tokens']}")


def main():
    """Pokreće interaktivno ili jednokratno postavljanje pitanja."""
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?")
    parser.add_argument("--k", type=int, default=TOP_K)
    parser.add_argument("--max-distance", type=float, default=MAX_DISTANCE)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    collection = get_collection()
    if args.question is not None:
        show(
            args.question,
            answer(collection, args.question, args.k, args.max_distance),
            args.debug,
        )
        return

    while True:
        question = input("Question (empty line to quit): ")
        if not question:
            break
        show(
            question,
            answer(collection, question, args.k, args.max_distance),
            args.debug,
        )


if __name__ == "__main__":
    main()
