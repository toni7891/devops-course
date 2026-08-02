from flask import Flask, jsonify, abort
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


# ── global error handlers ─────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": {"message": "Resource not found", "code": "NOT_FOUND"}
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": {"message": "Bad request", "code": "BAD_REQUEST"}
    }), 400


@app.errorhandler(Exception)
def handle_exception(error):
    # Pass through HTTP errors to their specific handlers first
    if isinstance(error, HTTPException):
        return jsonify({
            "success": False,
            "error": {"message": error.description, "code": str(error.code)}
        }), error.code

    # Unexpected exceptions — log and return 500
    print(f"[ERROR] Unhandled exception: {error}")
    return jsonify({
        "success": False,
        "error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}
    }), 500


# ── demo routes ───────────────────────────────────────────────────────────────

@app.route("/abort-demo/<int:item_id>")
def abort_demo(item_id):
    # Simulate a lookup that finds nothing
    fake_db = {1: "apple", 2: "banana"}
    item = fake_db.get(item_id)
    if item is None:
        abort(404)
    return jsonify({"success": True, "data": item})


@app.route("/crash")
def crash():
    # Intentional bug — triggers the catch-all handler
    result = 1 / 0
    return jsonify({"data": result})


if __name__ == "__main__":
    app.run(debug=True)
