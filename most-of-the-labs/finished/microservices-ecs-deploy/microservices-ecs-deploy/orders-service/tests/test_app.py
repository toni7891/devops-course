from unittest.mock import patch

import requests
from app import app


def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200


@patch("app.requests.get")
def test_order_confirmed(mock_get):
    mock_get.return_value.json.return_value = {"sku": "widget", "quantity": 10}
    mock_get.return_value.raise_for_status.return_value = None

    client = app.test_client()
    resp = client.post("/orders", json={"sku": "widget", "quantity": 2})

    assert resp.status_code == 200
    assert resp.get_json()["status"] == "confirmed"


@patch("app.requests.get")
def test_order_backordered(mock_get):
    mock_get.return_value.json.return_value = {"sku": "gadget", "quantity": 0}
    mock_get.return_value.raise_for_status.return_value = None

    client = app.test_client()
    resp = client.post("/orders", json={"sku": "gadget", "quantity": 2})

    assert resp.status_code == 200
    assert resp.get_json()["status"] == "backordered"


@patch("app.requests.get")
def test_order_inventory_unavailable(mock_get):
    mock_get.side_effect = requests.ConnectionError()

    client = app.test_client()
    resp = client.post("/orders", json={"sku": "widget", "quantity": 1})

    assert resp.status_code == 503
