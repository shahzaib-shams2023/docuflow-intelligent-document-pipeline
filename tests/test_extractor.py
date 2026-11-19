import asyncio
from app.extractor.llm_extractor import DocumentExtractor
from app.samples import SAMPLE_INVOICES


def test_extract_clean_invoice():
    async def run():
        raw = SAMPLE_INVOICES["clean_software_invoice"]
        return await DocumentExtractor.extract_invoice(raw)

    inv = asyncio.run(run())
    assert "INV-2024-8841" in inv.invoice_number
    assert inv.vendor.name != ""
    assert len(inv.line_items) >= 3
    assert inv.financials.subtotal == 3500.00
    assert inv.financials.total_amount == 3780.00

