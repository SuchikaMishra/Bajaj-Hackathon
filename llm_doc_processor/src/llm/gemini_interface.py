# src/llm/gemini_interface.py

import google.generativeai as genai

def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("models/gemini-1.5-flash")

def ask_gemini(model, query, context=""):
    """General purpose function for asking Gemini questions with optional context"""
    if context:
        prompt = f"""
{query}

Context:
{context}
"""
    else:
        prompt = query
    
    response = model.generate_content(prompt)
    return response.text.strip()

def ask_gemini_insurance_claim(model, query, top_clauses):
    """Specialized function for insurance claim analysis"""
    prompt = f"""
You are an insurance claim analyst. Based on the following user's query and the policy clauses, respond with a clear structured JSON including:

- "decision": "Approved" or "Rejected"
- "amount": (optional, if mentioned)
- "justification": clearly mention which clause(s) apply and why

User Query:
"{query}"

Policy Clauses:
{top_clauses}

Return only the JSON. Don't add explanations or introductions.
"""
    response = model.generate_content(prompt)
    return response.text.strip()
