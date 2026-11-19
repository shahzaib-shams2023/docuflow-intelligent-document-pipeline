import asyncio
from app.extractor.llm_extractor import DocumentExtractor
from app.validator.ledger_reconciler import LedgerReconciler
from app.samples import SAMPLE_INVOICES


def test_reconcile_clean_invoice_passes():
    async def run():
        raw = SAMPLE_INVOICES["clean_software_invoice"]
        return await DocumentExtractor.extract_invoice(raw)

    inv = asyncio.run(run())
    audit = LedgerReconciler.audit_invoice(inv)
    assert audit.is_mathematically_valid is True
    assert audit.discrepancy_amount <= 0.05
    assert audit.review_status == "AUTO_APPROVED"
    assert len(audit.validation_errors) == 0


def test_reconcile_invoice_with_discrepancy():
    async def run():
        raw = SAMPLE_INVOICES["invoice_with_math_discrepancy"]
        return await DocumentExtractor.extract_invoice(raw)

    inv = asyncio.run(run())
    audit = LedgerReconciler.audit_invoice(inv)
    assert audit.is_mathematically_valid is False
    assert audit.review_status == "NEEDS_HUMAN_REVIEW"
    assert len(audit.validation_errors) > 0

