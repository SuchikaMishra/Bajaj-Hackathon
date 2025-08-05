# src/main.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from dotenv import load_dotenv
from src.extract.pdf_extractor import extract_pdf
from src.extract.docx_extractor import extract_docx
from src.llm.embedding import load_clauses, build_faiss_index, save_index
from src.llm.query_handler import handle_query
from src.llm.gemini_interface import init_gemini
from src.llm.insurance_analyzer import batch_analyze_chunks

load_dotenv()  # Load GEMINI_API_KEY from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

RAW_DOCS_DIR = "data/raw_docs"
PROCESSED_DOCS_DIR = "data/processed_docs"

os.makedirs(PROCESSED_DOCS_DIR, exist_ok=True)

def extract_documents():
    model = init_gemini(GEMINI_API_KEY)
    
    for file in os.listdir(RAW_DOCS_DIR):
        filepath = os.path.join(RAW_DOCS_DIR, file)
        filename = os.path.splitext(file)[0]

        # Extract raw document data
        if file.lower().endswith(".pdf"):
            raw_chunks = extract_pdf(filepath)
        elif file.lower().endswith(".docx"):
            raw_chunks = extract_docx(filepath)
        else:
            continue

        # Save raw extracted data
        with open(os.path.join(PROCESSED_DOCS_DIR, f"{filename}.json"), "w") as f:
            json.dump(raw_chunks, f, indent=2)

        # Analyze chunks with insurance-specific processing
        print(f"🔍 Analyzing {file} with insurance AI...")
        analyzed_chunks = batch_analyze_chunks(raw_chunks, model)
        
        # Prepare processed data structure
        processed_data = {
            "source_file": file,
            "total_chunks": len(analyzed_chunks),
            "analyzed_chunks": []
        }
        
        # Combine raw and analyzed data
        for i, (raw_chunk, analyzed_chunk) in enumerate(zip(raw_chunks, analyzed_chunks)):
            combined_chunk = {
                "chunk_id": i,
                "source_file": file,
                "raw_data": raw_chunk,
                "analysis": analyzed_chunk
            }
            processed_data["analyzed_chunks"].append(combined_chunk)

        # Save analyzed data
        analyzed_filename = f"{filename}_analyzed.json"
        with open(os.path.join(PROCESSED_DOCS_DIR, analyzed_filename), "w") as f:
            json.dump(processed_data, f, indent=2)

        print(f"[✓] Extracted & Analyzed: {file} ({len(analyzed_chunks)} chunks)")

    print("[✓] All documents processed with insurance analysis!")

def build_semantic_index():
    corpus, _ = load_clauses(PROCESSED_DOCS_DIR)
    index, _, _ = build_faiss_index(corpus)
    save_index(index)
    print("[✓] FAISS index built and saved.")

def run_query_loop():
    model = init_gemini(GEMINI_API_KEY)
    while True:
        query = input("\nEnter your query (or type 'exit'): ").strip()
        if query.lower() == 'exit':
            break
        result = handle_query(query, model)
        print("\n🔍 LLM Response:")
        print(result)

if __name__ == "__main__":
    print("📄 Extracting Documents...")
    extract_documents()

    print("🔎 Building Embedding Index...")
    build_semantic_index()

    print("🤖 Ready for Queries!")
    run_query_loop()
