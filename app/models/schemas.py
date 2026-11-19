from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float


class VendorInfo(BaseModel):
    name: str
    tax_id: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None


class FinancialSummary(BaseModel):
    subtotal: float
    tax_rate_percent: Optional[float] = 0.0
    tax_amount: float = 0.0
    shipping_amount: float = 0.0
    total_amount: float
    currency: str = "USD"


class InvoiceData(BaseModel):
    invoice_number: str
    issue_date: str
    due_date: Optional[str] = None
    vendor: VendorInfo
    customer_name: Optional[str] = None
    line_items: List[LineItem]
    financials: FinancialSummary


class ValidationAudit(BaseModel):
    is_mathematically_valid: bool
    calculated_subtotal: float
    calculated_total: float
    discrepancy_amount: float
    validation_errors: List[str]
    compliance_flags: List[str]
    confidence_score: float
    review_status: str  # AUTO_APPROVED, NEEDS_HUMAN_REVIEW, REJECTED


class ExtractionResponse(BaseModel):
    raw_document_length: int
    invoice: InvoiceData
    audit: ValidationAudit
    processing_time_ms: float
    extracted_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ExtractRequest(BaseModel):
    document_text: str = Field(..., min_length=20, description="Raw OCR or text transcription of invoice")
    file_name: Optional[str] = "invoice.txt"

