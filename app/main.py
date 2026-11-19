from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import time
import os

from app.config import settings
from app.models.schemas import ExtractRequest, ExtractionResponse, InvoiceData
from app.extractor.ocr_normalizer import OCRNormalizer
from app.extractor.llm_extractor import DocumentExtractor
from app.validator.ledger_reconciler import LedgerReconciler
from app.samples import SAMPLE_INVOICES

app = FastAPI(
    title=settings.app_name,
    description="Intelligent Document Processing & Invoice Extraction Pipeline with Ledger Reconciliation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "DocuFlow Invoice Extraction Pipeline API is active."}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.environment,
        "llm_mode": "online" if settings.llm_api_key else "deterministic-fallback"
    }


@app.get("/api/samples")
async def get_invoice_samples():
    return SAMPLE_INVOICES


@app.post("/api/extract", response_model=ExtractionResponse)
async def extract_invoice_document(request: ExtractRequest):
    start_time = time.time()
    try:
        # Step 1: Normalize text & strip OCR noise
        clean_text = OCRNormalizer.normalize_text(request.document_text)

        # Step 2: Extract structured invoice schema
        invoice = await DocumentExtractor.extract_invoice(clean_text)

        # Step 3: Perform mathematical ledger reconciliation
        audit = LedgerReconciler.audit_invoice(invoice)

        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return ExtractionResponse(
            raw_document_length=len(request.document_text),
            invoice=invoice,
            audit=audit,
            processing_time_ms=elapsed_ms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document extraction failure: {str(e)}")


@app.post("/api/export")
async def export_to_erp(invoice: InvoiceData):
    """Generates standard ERP JSON payload (SAP / QuickBooks compatible)."""
    return {
        "erp_format": "SAP_B1_INVOICE_V2",
        "sync_status": "QUEUED_FOR_ERP_POST",
        "payload": {
            "DocType": "dDocument_Item",
            "DocDate": invoice.issue_date,
            "DocDueDate": invoice.due_date or invoice.issue_date,
            "CardCode": f"VEND-{invoice.vendor.name[:6].upper()}",
            "CardName": invoice.vendor.name,
            "DocumentLines": [
                {
                    "ItemDescription": item.description,
                    "Quantity": item.quantity,
                    "UnitPrice": item.unit_price,
                    "LineTotal": item.total
                }
                for item in invoice.line_items
            ],
            "DocTotal": invoice.financials.total_amount,
            "VatSum": invoice.financials.tax_amount
        }
    }

