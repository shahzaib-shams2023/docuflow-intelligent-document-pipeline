# DocuFlow: Intelligent Document & Invoice Processing Pipeline

DocuFlow is a production-grade Intelligent Document Processing (IDP) and invoice extraction pipeline designed to automate unstructured financial document processing, enforce mathematical ledger reconciliation, and synchronize structured records with ERP accounting platforms.

---

## 🔍 The Problem
Enterprise accounts payable teams process millions of invoices, receipts, and purchase orders annually. Manual transcription and generic OCR systems suffer from critical weaknesses:
- **High Error Rates**: Small transcription errors in quantities or decimal points cause compounding accounting discrepancies.
- **Lack of Arithmetic Verification**: Standard AI extraction does not verify whether line items mathematically sum to stated subtotals and totals.
- **Unstructured Format Variance**: Vendors submit wildly differing layouts, tax codes, and currency notations that break rigid template scrapers.

## 💡 The Solution
DocuFlow provides an automated pipeline combining OCR normalization, schema-constrained LLM extraction, and strict ledger auditing:
1. **OCR Text Normalization**: Cleans whitespace, standardized currency codes, and formats unstructured text blocks.
2. **Pydantic Schema Extraction**: Extracts vendor metadata, invoice numbers, dates, line item tables, taxes, and financial totals into typed schemas.
3. **Mathematical Ledger Reconciliation**: Verifies `quantity * unit_price == total`, `sum(line_totals) == subtotal`, and `subtotal + tax + shipping == total_amount`.
4. **Human-in-the-Loop Routing**: Automatically approves mathematically consistent invoices with high confidence while routing discrepancies to an exception queue.
5. **ERP Accounting Sync**: Formats approved invoices into standardized payloads compatible with SAP Business One, QuickBooks, and NetSuite.

---

## 🏛️ System Architecture

```
Raw Invoice / Receipt (Text, PDF Dump, OCR)
                   │
                   ▼
       [OCR Text Normalizer]
                   │
                   ▼
      [Schema-Constrained LLM]
                   │
                   ▼
   [Mathematical Ledger Reconciler]
    - Line item cross-multiplication
    - Subtotal & tax ledger check
    - Discrepancy cents calculation
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
  [AUTO_APPROVED]    [NEEDS_HUMAN_REVIEW]
         │
         ▼
  [ERP Sync Engine] (SAP / QuickBooks JSON)
```

---

## 🛠️ Technology Stack
- **Backend**: Python 3.11, FastAPI, Pydantic v2
- **Validation**: Mathematical Ledger Engine & Accounting Rules
- **Testing**: Pytest, Starlette TestClient
- **Frontend**: Responsive Document Studio (Tailwind CSS, FontAwesome)
- **Deployment**: Docker, Docker Compose, GitHub Actions CI

---

## 🚀 Getting Started

### Installation
```bash
cd docuflow-intelligent-document-pipeline

# Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Optional: set `LLM_API_KEY` to connect OpenAI, Groq, or OpenRouter. Without an API key, DocuFlow runs seamlessly in its deterministic extraction mode.

### Running the Application
```bash
python -m uvicorn app.main:app --reload --port 8003
```
Access the Document Processing Studio at `http://localhost:8003` or view the OpenAPI documentation at `http://localhost:8003/docs`.

---

## 🧪 Running Automated Tests
```bash
pytest tests/ -v
```

---

## 🐳 Docker Deployment
```bash
docker compose up --build
```
The application will be accessible at `http://localhost:8003`.

---

## 📡 API Reference

### Extract Invoice
`POST /api/extract`
```json
{
  "document_text": "INVOICE: INV-2024-8841\nDate: 2024-11-10\n..."
}
```

Response:
```json
{
  "raw_document_length": 580,
  "invoice": {
    "invoice_number": "INV-2024-8841",
    "issue_date": "2024-11-10",
    "vendor": { "name": "NexSphere Cloud Technologies Inc.", "tax_id": "US-EIN-8849102" },
    "line_items": [
      { "description": "Kubernetes Production Cluster Node", "quantity": 2.0, "unit_price": 1200.0, "total": 2400.0 }
    ],
    "financials": {
      "subtotal": 3500.0,
      "tax_amount": 280.0,
      "total_amount": 3780.0
    }
  },
  "audit": {
    "is_mathematically_valid": true,
    "calculated_total": 3780.0,
    "discrepancy_amount": 0.0,
    "review_status": "AUTO_APPROVED",
    "confidence_score": 0.96
  }
}
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

