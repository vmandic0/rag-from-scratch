# Osnovni URL Ollama servisa; lokalna podrazumevana adresa je najčešća postavka.
OLLAMA_URL = "http://localhost:11434"

# Model za ugnježđavanje; nomic-embed-text je namenjen semantičkoj pretrazi.
EMBED_MODEL = "nomic-embed-text"

# Jezički model; mali model daje dobar balans brzine i kvaliteta za lokalni rad.
LLM_MODEL = "llama3.2:1b"

# Direktorijum sa dokumentima; sadržaj projekta se čuva u ovoj fascikli.
DOCS_DIR = "docs"

# Direktorijum Chroma baze; odvaja vektorsku bazu od izvornog sadržaja.
DB_DIR = "chroma_db"

# Naziv kolekcije; jasno identifikuje skup znanja aplikacije.
COLLECTION = "knowledge"

# Broj reči po odlomku; dovoljno velik za kontekst uz razumnu preciznost.
CHUNK_WORDS = 150

# Preklapanje odlomaka; čuva kontinuitet između susednih delova teksta.
CHUNK_OVERLAP = 30

# Broj najboljih rezultata; tri rezultata daju sažet relevantan kontekst.
TOP_K = 3

# Najveća dozvoljena udaljenost; odbacuje slabo povezane rezultate.
MAX_DISTANCE = 0.6

# Maksimalna dužina konteksta modela; 4096 tokena pokriva tipične upite.
NUM_CTX = 4096
