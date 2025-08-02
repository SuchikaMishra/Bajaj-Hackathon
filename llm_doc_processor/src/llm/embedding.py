# src/llm/embedding.py

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def load_clauses(json_folder):
    corpus = []
    metadata = []
    for file in os.listdir(json_folder):
        if file.endswith(".json"):
            with open(os.path.join(json_folder, file), 'r') as f:
                clauses = json.load(f)
                for clause in clauses:
                    corpus.append(clause["content"])
                    metadata.append(clause)
    return corpus, metadata

def build_faiss_index(corpus, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(corpus, convert_to_tensor=False)
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, embeddings, model

def save_index(index, path="models/faiss_index"):
    os.makedirs(path, exist_ok=True)
    faiss.write_index(index, os.path.join(path, "index.faiss"))

def load_index(path="models/faiss_index"):
    return faiss.read_index(os.path.join(path, "index.faiss"))
