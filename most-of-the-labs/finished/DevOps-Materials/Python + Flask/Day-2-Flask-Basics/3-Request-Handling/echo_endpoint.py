from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/echo", methods=["POST"])
def echo():
    body = request.json

    if body is None:
        return jsonify({"success": False, "error": "JSON body required"}), 400

    return jsonify({"success": True, "echo": body})


if __name__ == "__main__":
    app.run(debug=True)
