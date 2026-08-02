from app import app


def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_stock_known_sku():
    client = app.test_client()
    resp = client.get("/stock/widget")
    assert resp.status_code == 200
    assert resp.get_json() == {"sku": "widget", "quantity": 10}


def test_stock_unknown_sku():
    client = app.test_client()
    resp = client.get("/stock/unknown")
    assert resp.status_code == 200
    assert resp.get_json() == {"sku": "unknown", "quantity": 0}
