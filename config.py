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
#CHUNK_WORDS = 150

# Veličina chunka u rečima. Sekcije u docs/ imaju oko 40 reči, pa prozor od 40
# deli samo duže sekcije, a svaki chunk ostaje fokusiran na jednu temu.
# (Poređeno sa 150, gde je svaka sekcija tačno jedan chunk i prozor se ne koristi.)
# Izmereno (evaluate.py): 150/30 -> top-1 12/12, 40/10 -> top-1 X/12
CHUNK_WORDS = 40

# Preklapanje odlomaka; čuva kontinuitet između susednih delova teksta.
#CHUNK_OVERLAP = 30

# Preklapanje u rečima. 10 reči je 25% prozora: dovoljno da rečenica koju preseče
# granica chunkova ostane cela u bar jednom od njih, a da se tekst ne udvostruči.
# Izmereno (evaluate.py): 150/30 -> top-1 12/12, 40/10 -> top-1 X/12
CHUNK_OVERLAP = 10

# Broj najboljih rezultata; tri rezultata daju sažet relevantan kontekst.
TOP_K = 3

# Najveća dozvoljena udaljenost; odbacuje slabo povezane rezultate.
#MAX_DISTANCE = 0.6

# Najveća dozvoljena distanca; izmereno: relevantna pitanja 0.15-0.29,
# nerelevantna 0.41-0.51, pa je prag sredina razmaka (calibrate.py)
MAX_DISTANCE = 0.35

# Maksimalna dužina konteksta modela; 4096 tokena pokriva tipične upite.
NUM_CTX = 4096
