# src/llm/query_handler.py

import numpy as np
from src.llm.gemini_interface import ask_gemini
from src.llm.embedding import load_index, load_clauses
from sentence_transformers import SentenceTransformer

def handle_query(query, model_gemini):
    corpus, metadata = load_clauses("data/processed_docs")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = embedding_model.encode(query).reshape(1, -1)

    index = load_index()
    D, I = index.search(np.array(query_embedding), k=5)
    
    top_clauses = [metadata[i]["content"] for i in I[0] if i < len(metadata)]
    top_text = "\n\n".join([f"- {clause}" for clause in top_clauses])

    return ask_gemini(model_gemini, query, top_text)
