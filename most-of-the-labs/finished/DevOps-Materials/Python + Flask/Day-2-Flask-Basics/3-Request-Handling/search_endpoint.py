from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake data to search through
USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "Alice Smith"},
]


@app.route("/search")
def search():
    name = request.args.get("name")

    if not name:
        return jsonify({"success": False, "error": "name is required"}), 400

    results = [u for u in USERS if name.lower() in u["name"].lower()]
    return jsonify({"success": True, "query": name, "results": results})


if __name__ == "__main__":
    app.run(debug=True)
