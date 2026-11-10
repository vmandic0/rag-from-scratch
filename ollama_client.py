import requests

from config import EMBED_MODEL, LLM_MODEL, NUM_CTX, OLLAMA_URL


def embed(texts):
    """Generiše vektore za prosleđene tekstove."""
    response = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={"model": EMBED_MODEL, "input": texts},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["embeddings"]


def embed_documents(texts):
    """Generiše vektore dokumenata uz obavezni prefiks modela."""
    return embed([f"search_document: {text}" for text in texts])


def embed_query(text):
    """Generiše jedan vektor upita uz obavezni prefiks modela."""
    return embed([f"search_query: {text}"])[0]


def chat(system_prompt, user_prompt):
    """Šalje razgovor modelu i vraća odgovor i broj obrađenih tokena."""
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": 0, "num_ctx": NUM_CTX},
        },
        timeout=600,
    )
    response.raise_for_status()
    data = response.json()
    return (
        data["message"]["content"],
        data.get("prompt_eval_count"),
        data.get("eval_count"),
    )
