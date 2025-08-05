# src/llm/insurance_analyzer.py

import json
import re
from typing import Dict, List, Any, Optional

def analyze_insurance_chunk(chunk_data: Dict[str, Any], model) -> Dict[str, Any]:
    """Analyze insurance policy text chunk using LLM"""
    
    # Extract text content from the chunk
    chunk_text = chunk_data.get('content', '')
    heading = chunk_data.get('heading', '')
    clause_number = chunk_data.get('clause_number', '')
    
    # Build context for the chunk
    context_info = []
    if heading:
        context_info.append(f"Section: {heading}")
    if clause_number:
        context_info.append(f"Clause: {clause_number}")
    
    context = " | ".join(context_info) if context_info else "Unknown Section"
    
    prompt = f"""You are an AI insurance policy analyzer. You are reading a section of an insurance policy document.

Your task is to:
1. Summarize this section in 1-2 lines.
2. Identify any conditions, exclusions, or benefits mentioned.
3. Tag key medical terms, waiting periods, eligibility requirements, and clause numbers.
4. Prepare it for semantic search and reasoning.

Context: {context}

Text:
\"\"\"{chunk_text}\"\"\"

Respond in the following JSON format:
{{
  "summary": "Brief 1-2 line summary of this section",
  "key_points": [
    "Important condition or benefit 1",
    "Important condition or benefit 2"
  ],
  "tags": ["waiting period", "medical condition", "age limit", "coverage exclusion"],
  "clause_reference": "{context}"
}}

Important: Return ONLY the JSON object, no additional text."""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Find JSON in response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON found in response")
            
        json_str = response_text[json_start:json_end]
        analyzed_data = json.loads(json_str)
        
        # Ensure all required fields exist
        analyzed_data.setdefault("summary", "")
        analyzed_data.setdefault("key_points", [])
        analyzed_data.setdefault("tags", [])
        analyzed_data.setdefault("clause_reference", context)
        
        return analyzed_data
        
    except Exception as e:
        print(f"Error analyzing chunk: {e}")
        return {
            "summary": f"Error analyzing section: {heading} {clause_number}".strip(),
            "key_points": [chunk_text[:100] + "..." if len(chunk_text) > 100 else chunk_text],
            "tags": ["analysis_failed"],
            "clause_reference": context,
            "error": str(e)
        }

def batch_analyze_chunks(chunks: List[Dict[str, Any]], model, batch_size: int = 5) -> List[Dict[str, Any]]:
    """Analyze multiple chunks in batches to avoid rate limiting"""
    analyzed_chunks = []
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Analyzing batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}...")
        
        for chunk in batch:
            analyzed_chunk = analyze_insurance_chunk(chunk, model)
            analyzed_chunks.append(analyzed_chunk)
    
    return analyzed_chunks

def extract_key_insurance_terms(text: str) -> List[str]:
    """Extract common insurance terms from text"""
    insurance_terms = [
        r'waiting period', r'deductible', r'premium', r'coverage', r'exclusion',
        r'pre-existing condition', r'claim', r'beneficiary', r'policy holder',
        r'maternity', r'hospitalization', r'outpatient', r'co-pay', r'co-insurance',
        r'annual limit', r'lifetime limit', r'network provider', r'emergency',
        r'critical illness', r'disability', r'accidental', r'dental', r'vision',
        r'prescription', r'preventive care', r'specialist', r'diagnostic',
        r'age limit', r'geographical', r'renewal', r'termination'
    ]
    
    found_terms = []
    text_lower = text.lower()
    
    for term in insurance_terms:
        if re.search(term, text_lower):
            found_terms.append(term.replace(r'', ''))
    
    return found_terms
