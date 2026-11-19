import pytest
from app.extractor.ocr_normalizer import OCRNormalizer


def test_normalize_ocr_text():
    raw = "INVOICE   #101\r\nUS$ 500.00   \n\n\n\nTotal: USD 500.00"
    cleaned = OCRNormalizer.normalize_text(raw)
    assert "\r" not in cleaned
    assert "$ 500.00" in cleaned
    assert "US$" not in cleaned
    assert "USD " not in cleaned
    assert "\n\n\n" not in cleaned

