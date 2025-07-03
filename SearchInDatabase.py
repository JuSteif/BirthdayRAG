import json
import os
from typing import List, Tuple

import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

def build_index(
        json_path: str = os.getenv("DATASET_PATH"),
        model_name: str = os.getenv("MODEL_ST")
) -> Tuple[faiss.IndexFlatIP, List[dict], SentenceTransformer]:
    """
    Lädt Datensätze, Modell und erstellt einen FAISS-Index
    mit normalisierten Embeddings (Cosine-Similarity via Inner Product).
    Gibt Index, Rohdatenliste und das geladene Modell zurück.
    """
    # 1) Daten einlesen
    with open(json_path, "r", encoding="utf-8") as f:      # json.load best practice :contentReference[oaicite:3]{index=3}
        records: List[dict] = json.load(f)

    # 2) Modell laden
    model = SentenceTransformer(model_name)                 # 384 Dims, flott & klein :contentReference[oaicite:4]{index=4}

    # 3) Texte erstellen & Embeddings berechnen
    def rec_to_text(rec):
        return f"{rec['firstname']} {rec['lastname']} " \
               f"{rec['day']:02d}.{rec['month']:02d}.{rec['year']}"
    corpus_texts = [rec_to_text(r) for r in records]

    emb = model.encode(
        corpus_texts,
        convert_to_numpy=True,
        normalize_embeddings=True   # Cosine ≈ Inner Product :contentReference[oaicite:5]{index=5}
    )

    # 4) FAISS‑Index anlegen
    dim = emb.shape[1]
    index = faiss.IndexFlatIP(dim)                           # exakt & für kleine Corpora ausreichend :contentReference[oaicite:6]{index=6}
    index.add(emb.astype(np.float32))

    return index, records, model



def search_entries(
        query: str,
        index: faiss.IndexFlatIP,
        records: List[dict],
        model: SentenceTransformer,
        k_env_var: str = os.getenv("NUM_RESULTS")
) -> str:
    """
    Führt eine semantische Suche durch und liefert die Top‑k Ergebnisse
    als JSON‑String zurück. k wird aus der Umgebungsvariable NUM_RESULTS
    (oder dem in k_env_var übergebenen Namen) bezogen.
    """
    # 1) Konfiguration laden

    k = int(k_env_var)

    # 2) Query‑Embedding
    q_emb = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)

    # 3) FAISS‑Suche
    distances, idx = index.search(q_emb, k)                 # Standard‑API :contentReference[oaicite:9]{index=9}

    # 4) Treffer extrahieren
    hits = [records[i] for i in idx[0] if i != -1]
    return json.dumps(hits, ensure_ascii=False)