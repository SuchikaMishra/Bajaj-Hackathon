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
    
    # Build context from analyzed insurance data
    context_parts = []
    for i in I[0]:
        if i < len(metadata):
            chunk = metadata[i]
            analysis = chunk.get("analysis", {})
            
            context_part = f"""
**{analysis.get('clause_reference', 'Unknown Section')}**
Summary: {analysis.get('summary', 'No summary available')}
Key Points: {', '.join(analysis.get('key_points', []))}
Tags: {', '.join(analysis.get('tags', []))}
Original Content: {chunk.get('raw_content', '')[:200]}...
"""
            context_parts.append(context_part)
    
    context = "\n".join(context_parts)
    
    enhanced_prompt = f"""Based on the following insurance policy information, provide a comprehensive answer to the user's query:

INSURANCE POLICY CONTEXT:
{context}

USER QUERY: {query}

Please provide a clear, accurate response based on the policy information above. Include relevant clause references and specific conditions when applicable."""

    return ask_gemini(model_gemini, enhanced_prompt, "")
