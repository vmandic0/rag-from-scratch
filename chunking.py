import re


def split_sections(text):
    """Deli Markdown tekst na odeljke prema naslovima."""
    sections = []
    title = "Introduction"
    lines = []

    for line in text.splitlines():
        if re.match(r"^#{1,3}\s", line):
            body = "\n".join(lines).strip()
            if body:
                sections.append((title, body))
            title = line.lstrip("#").strip()
            lines = []
        else:
            lines.append(line)

    body = "\n".join(lines).strip()
    if body:
        sections.append((title, body))

    return sections


def split_words(text, max_words, overlap):
    """Deli tekst na preklapajuće prozore ograničene brojem reči."""
    words = text.split()
    if overlap >= max_words:
        raise ValueError("Preklapanje mora biti manje od maksimalnog broja reči.")
    if len(words) <= max_words:
        return [text]

    step = max_words - overlap
    chunks = []
    start = 0
    while True:
        chunks.append(" ".join(words[start:start + max_words]))
        if start + max_words >= len(words):
            break
        start += step

    return chunks


def chunk_document(text, max_words, overlap):
    """Deli dokument na označene tekstualne delove za ugnježđavanje."""
    chunks = []
    for title, body in split_sections(text):
        for piece in split_words(body, max_words, overlap):
            chunks.append({"section": title, "text": title + "\n" + piece})
    return chunks
