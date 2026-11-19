from fastapi.testclient import TestClient
from app.main import app
from app.samples import SAMPLE_INVOICES

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"


def test_samples():
    res = client.get("/api/samples")
    assert res.status_code == 200
    data = res.json()
    assert "clean_software_invoice" in data


def test_extract_endpoint():
    payload = {
        "document_text": SAMPLE_INVOICES["clean_software_invoice"]
    }
    res = client.post("/api/extract", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "invoice" in data
    assert "audit" in data
    assert data["audit"]["is_mathematically_valid"] is True

    # Test export
    export_res = client.post("/api/export", json=data["invoice"])
    assert export_res.status_code == 200
    export_data = export_res.json()
    assert export_data["sync_status"] == "QUEUED_FOR_ERP_POST"

