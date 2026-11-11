# rag-from-scratch

Lokalni RAG sistem napisan od nule (Ollama + ChromaDB). Odgovara na pitanja iz Markdown dokumenata u fascikli `docs/` i navodi izvore.

## Kako radi

**Faza 1 (`ingest.py`):** `docs/*.md` se deli po naslovima (`##`), zatim kliznim prozorom od 40 reči sa preklapanjem od 10 reči (`chunking.py`). Dobijaju se embedding-i pomoću modela `nomic-embed-text`, uz prefikse `"search_document:"` za dokumente i `"search_query:"` za pitanja, a zatim se čuvaju u ChromaDB-u sa kosinusnom udaljenošću. Otisak fajla (sadržaj i parametri chunkovanja) sprečava ponovnu obradu nepromenjenih fajlova.

**Faza 2 (`ask.py`):** embedding pitanja -> 3 najbliža chunka -> odbacuju se chunkovi sa udaljenošću većom od 0.35 (ako nijedan ne ostane, model se ne poziva i odgovor je `"I could not find this in the provided documents."`) -> prompt -> `llama3.2:1b` (temperatura 0) -> odgovor. Izvore dodaje kod na osnovu korišćenih chunkova, a ne model.

## Pokretanje
Ollama mora biti instalirana i pokrenuta.

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:1b
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ingest.py --reset
python ask.py "Which status code means a resource was created?" --debug
python evaluate.py
```

## Struktura repoa

- `config.py` (parametri)
- `ollama_client.py` (embedding-i i chat preko Ollama REST API-ja)
- `chunking.py` (deljenje dokumenata)
- `ingest.py` (faza 1)
- `ask.py` (faza 2)
- `calibrate.py` (merenje praga)
- `evaluate.py` (evaluacija)
- `docs/` (7 Markdown fajlova: statistika, testiranje hipoteza, mašinsko učenje, neuronske mreže, HTTP/REST, Git, baze podataka/SQL)
- `requirements.txt`

## Merenje praga (`calibrate.py`)

Relevantna pitanja imaju udaljenosti 0.15-0.29, a irelevantna 0.41-0.51. Prag 0.35 je sredina tog razmaka. Ranija vrednost 0.6 nije odbacivala nijedan rezultat.

## Evaluacija (`evaluate.py`: 12 pitanja sa odgovorom i 4 bez odgovora)

| Parametri | Chunkova | Top-1 | Top-k | Ključna reč u odgovoru | Tačna odbijanja | Odgovori samo sa tačnim izvorom |
|---|---:|---:|---:|---:|---:|---:|
| 150/30 | 35 | 12/12 | 12/12 | 12/12 | 4/4 | 8/12 |
| 40/10 | 52 | 12/12 | 12/12 | 12/12 | 4/4 | 11/12 |

Izabrano je 40/10, jer su citirani izvori čistiji (manji chunkovi su fokusiraniji, pa manje chunkova iz drugih tema prolazi prag).

## Odluke koje sam doneo

- Izvore dodaje kod, jer je 1B model ponekad ispisivao samo `"[file.md]"` bez odgovora.
- Prompt daje prednost odgovaranju, a odbijanje je izuzetak; prva verzija je odbijala odgovor čak i kada je kontekst sadržao odgovor.
- Prag je izmeren, a ne pretpostavljen.
- Kolekcija koristi kosinusnu udaljenost (Chroma podrazumevano koristi L2, pa je kosinus eksplicitno podešen).

## Ograničenja

- Mali korpus (35 do 52 chunka) i pitanja koja sam napisao, pa su metrike zasićene (12/12) i ne razlikuju konfiguracije.
- Provera ključne reči ne dokazuje da je odgovor tačan: odgovor o Besselovoj korekciji sadrži izmišljeni deo koji nije u dokumentu.
- Svi korišćeni chunkovi se navode kao izvori, a ne samo onaj koji je sadržao odgovor.
- 1B model ponekad halucinira ili parafrazira previše uopšteno.

## Moguća poboljšanja

- Izvori samo iz chunka koji je stvarno odgovorio (ili relativni prag: samo chunkovi unutar 0.05 od najboljeg).
- Veći model (npr. `llama3.2:3b`) zbog halucinacija.
- Veći korpus i više pitanja za evaluaciju, uključujući parafrazirana, da metrike razlikuju konfiguracije.
- Meša pretragu po ključnim rečima i embedding-a (hybrid search).

## Primer

​```
$ python ask.py "What is the default port for HTTPS?"
Q: What is the default port for HTTPS?
A: The default port for HTTPS is 443. [web_http_rest.md]
​```