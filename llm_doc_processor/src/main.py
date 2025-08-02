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

load_dotenv()  # Load GEMINI_API_KEY from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

RAW_DOCS_DIR = "data/raw_docs"
PROCESSED_DOCS_DIR = "data/processed_docs"

os.makedirs(PROCESSED_DOCS_DIR, exist_ok=True)

def extract_documents():
    for file in os.listdir(RAW_DOCS_DIR):
        filepath = os.path.join(RAW_DOCS_DIR, file)
        filename = os.path.splitext(file)[0]

        if file.lower().endswith(".pdf"):
            data = extract_pdf(filepath)
        elif file.lower().endswith(".docx"):
            data = extract_docx(filepath)
        else:
            continue

        with open(os.path.join(PROCESSED_DOCS_DIR, f"{filename}.json"), "w") as f:
            json.dump(data, f, indent=2)

        print(f"[✓] Extracted: {file}")

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
