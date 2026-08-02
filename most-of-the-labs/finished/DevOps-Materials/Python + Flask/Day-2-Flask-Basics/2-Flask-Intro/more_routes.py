from datetime import datetime, timezone
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "API is running"})


@app.route("/status")
def status():
    return jsonify({"status": "ok", "version": "1.0"})


@app.route("/time")
def current_time():
    now = datetime.now(timezone.utc).isoformat()
    return jsonify({"time": now})


@app.route("/info")
def info():
    return jsonify({
        "app": "Flask Practice",
        "author": "Student",
        "day": 2
    })


if __name__ == "__main__":
    app.run(debug=True)
