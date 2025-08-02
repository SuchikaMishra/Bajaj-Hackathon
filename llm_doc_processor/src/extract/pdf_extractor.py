import pdfplumber
import os
import json
import re
from pathlib import Path

def extract_pdf(pdf_path):
    extracted_clauses = []
    current_clause = {
        "heading": None,
        "clause_number": None,
        "content": "",
        "page": None
    }
    buffer = []
    current_heading = None

    # Patterns
    heading_pattern = re.compile(r'^[A-Z][A-Z\s\d\.\-]{4,}$')  # ALL CAPS headings
    clause_pattern = re.compile(r'^(\d+(\.\d+)*)([\)\.:])?\s+(.*)')  # 3.1 or 5.2: style

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                line = line.strip()

                # Skip empty or junk lines
                if not line or len(line) < 5:
                    continue

                # Detect new heading
                if heading_pattern.match(line) and not clause_pattern.match(line):
                    current_heading = line.title()  # Save as title case
                    continue

                # Detect new clause
                match = clause_pattern.match(line)
                if match:
                    # Save previous clause
                    if current_clause["clause_number"] or current_clause["content"]:
                        current_clause["content"] = ' '.join(buffer).strip()
                        if current_clause["content"]:
                            extracted_clauses.append(current_clause.copy())
                        buffer.clear()

                    clause_number = match.group(1)
                    content_start = match.group(4)

                    current_clause = {
                        "heading": current_heading,
                        "clause_number": clause_number,
                        "content": "",
                        "page": page_num
                    }
                    buffer.append(content_start)

                else:
                    # Continuation of previous clause
                    buffer.append(line)

    # Save last clause
    if buffer:
        current_clause["content"] = ' '.join(buffer).strip()
        if current_clause["content"]:
            extracted_clauses.append(current_clause.copy())

    return extracted_clauses


if __name__ == "__main__":
    input_dir = "data/raw_docs"
    output_dir = "data/processed_docs"
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            data = extract_pdf(pdf_path)

            output_path = os.path.join(output_dir, f"{Path(file).stem}.json")
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"✅ Extracted PDF: {file}")
