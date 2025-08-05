# Insurance Policy Analyzer

An AI-powered document processing system specifically designed for analyzing insurance policy documents using Gemini AI and semantic search.

## 🎯 Key Features

### ✅ What You Have Now
- **Smart Insurance Analysis**: Each document chunk is analyzed with AI to extract:
  - 📝 **Summary**: Concise 1-2 line summaries
  - 🎯 **Key Points**: Important conditions, exclusions, and benefits
  - 🏷️ **Tags**: Medical terms, waiting periods, eligibility requirements
  - 📍 **Clause References**: Section and clause number tracking

- **Enhanced Semantic Search**: Uses analyzed summaries and key points for better search relevance
- **Structured Output**: JSON format compatible with downstream processing
- **Batch Processing**: Handles multiple documents efficiently

### 🔄 What Changed from Your Original Code

#### Before (Basic Extraction):
```python
def extract_documents():
    for file in os.listdir(RAW_DOCS_DIR):
        # Extract raw text chunks
        data = extract_pdf(filepath)
        # Save basic JSON
        json.dump(data, f, indent=2)
```

#### After (AI-Powered Analysis):
```python
def extract_documents():
    model = init_gemini(GEMINI_API_KEY)
    for file in os.listdir(RAW_DOCS_DIR):
        # Extract raw text chunks
        raw_chunks = extract_pdf(filepath)
        # 🔍 NEW: Analyze with AI
        analyzed_chunks = batch_analyze_chunks(raw_chunks, model)
        # Save structured analysis + raw data
        processed_data = {
            "source_file": file,
            "analyzed_chunks": [combined_chunk_data]
        }
```

## 🏗️ Architecture

```
Raw PDF/DOCX → Text Extraction → AI Analysis → Structured JSON → Semantic Index → Smart Queries
     ↓              ↓              ↓              ↓              ↓             ↓
   📄 PDFs    📋 Text Chunks  🤖 Gemini AI   📊 Analysis   🔍 FAISS     💬 Q&A
```

## 🔧 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Gemini API
```bash
# Copy the template
cp .env.template .env

# Edit .env and add your API key
GEMINI_API_KEY=your_actual_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Run the System
```bash
# Full pipeline
python src/main.py

# Demo mode (analyze first 2 chunks)
python demo_insurance_analyzer.py
```

## 📊 Output Format

### Raw Extraction (unchanged):
```json
[
  {
    "heading": "Air Ambulance Cover",
    "clause_number": "1",
    "content": "In consideration of the payment...",
    "page": 2
  }
]
```

### 🆕 AI Analysis Output:
```json
{
  "source_file": "EDLHLGA23009V012223.pdf",
  "total_chunks": 25,
  "analyzed_chunks": [
    {
      "chunk_id": 0,
      "source_file": "EDLHLGA23009V012223.pdf",
      "raw_data": { /* original extracted data */ },
      "analysis": {
        "summary": "Air ambulance coverage for life-threatening emergencies up to 150km distance",
        "key_points": [
          "Maximum 150km travel distance covered",
          "Life-threatening emergency conditions only",
          "Licensed air ambulance required"
        ],
        "tags": ["air ambulance", "emergency", "distance limit", "150km"],
        "clause_reference": "Section 1"
      }
    }
  ]
}
```

## 🎯 Use Cases

### 1. **Claim Processing**
```python
query = "Is knee surgery covered for a 45-year-old patient?"
# Returns: Analysis based on relevant policy clauses with AI reasoning
```

### 2. **Policy Comparison**
```python
query = "What are the waiting periods for maternity benefits?"
# Returns: Structured comparison of waiting periods across policies
```

### 3. **Compliance Checking**
```python
query = "What exclusions apply to pre-existing conditions?"
# Returns: Complete list of exclusions with clause references
```

## 📁 Project Structure

```
llm_doc_processor/
├── 📄 src/main.py                    # Main pipeline (updated)
├── 🤖 src/llm/insurance_analyzer.py  # NEW: AI analysis module
├── 🔍 src/llm/query_handler.py       # Enhanced query handling
├── 📊 data/processed_docs/           # Raw + Analyzed outputs
├── 🎯 demo_insurance_analyzer.py     # NEW: Demo script
└── 📋 requirements.txt               # Updated dependencies
```

## 🚀 Next Steps

1. **Run the Demo**: `python demo_insurance_analyzer.py`
2. **Process Full Documents**: `python src/main.py`
3. **Test Queries**: Use the interactive query loop
4. **Extend Analysis**: Modify `insurance_analyzer.py` for domain-specific needs

## 🔍 Example Analysis Output

For the air ambulance clause, the AI now extracts:
- **Summary**: "Air ambulance coverage for emergencies within 150km"
- **Key Points**: ["Distance limited to 150km", "Life-threatening only", "Licensed providers required"]
- **Tags**: ["air ambulance", "emergency", "distance limit", "geographical restriction"]
- **Reference**: "Section 1"

This structured format enables much more intelligent querying and reasoning about insurance policies! 🎉
