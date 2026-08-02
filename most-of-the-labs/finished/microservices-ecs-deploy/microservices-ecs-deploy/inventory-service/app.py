from flask import Flask, jsonify

app = Flask(__name__)

STOCK = {
    "widget": 10,
    "gadget": 0,
}


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/stock/<sku>")
def stock(sku):
    return jsonify(sku=sku, quantity=STOCK.get(sku, 0))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
