# src/extract/docx_extractor.py

from docx import Document
import re
import os
import json
from pathlib import Path

def extract_docx(docx_path):
    doc = Document(docx_path)
    extracted_data = []
    buffer = []
    current_clause = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text or len(text) < 5:
            continue

        match = re.match(r"^(\d+(\.\d+)*)([\)\.:])?\s+(.*)", text)
        if match:
            if current_clause:
                current_clause["content"] = ' '.join(buffer).strip()
                extracted_data.append(current_clause.copy())
                buffer.clear()

            clause_number = match.group(1)
            content_start = match.group(4)
            current_clause = {
                "clause_number": clause_number,
                "heading": None,
                "content": "",
                "page": None
            }
            buffer.append(content_start)
        elif current_clause:
            buffer.append(text)

    if current_clause and buffer:
        current_clause["content"] = ' '.join(buffer).strip()
        extracted_data.append(current_clause)

    return extracted_data
