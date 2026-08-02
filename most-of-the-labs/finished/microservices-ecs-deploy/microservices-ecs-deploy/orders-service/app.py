import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

INVENTORY_URL = os.environ.get("INVENTORY_URL", "http://inventory:8080")


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/orders", methods=["POST"])
def create_order():
    order = request.get_json()
    sku = order["sku"]
    quantity = order["quantity"]

    try:
        resp = requests.get(f"{INVENTORY_URL}/stock/{sku}", timeout=3)
        resp.raise_for_status()
    except requests.RequestException:
        return jsonify(error="inventory service unavailable"), 503

    available = resp.json()["quantity"]
    status = "confirmed" if available >= quantity else "backordered"
    return jsonify(sku=sku, quantity=quantity, status=status)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
