from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
next_id = 1


@app.route("/tasks")
def get_tasks():
    return jsonify({"success": True, "data": tasks})


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    body = request.json
    if not body or not body.get("title"):
        return jsonify({"success": False, "error": "title is required"}), 400

    task = {
        "id": next_id,
        "title": body["title"],
        "completed": False,
    }
    tasks.append(task)
    next_id += 1

    return jsonify({"success": True, "data": task}), 201


if __name__ == "__main__":
    app.run(debug=True)
