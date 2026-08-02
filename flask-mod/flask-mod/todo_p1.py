from flask import Flask, jsonify, request 
app = Flask(__name__)

tasks = [
    {
        "id" : 1,
        "title" : "Learn Flask",
        "completed" : False
    },
    {
        "id" : 2,
        "title" : "Build API",
        "completed" : False
    },
    {
        "id" : 3,
        "title" : "Test with postman",
        "completed" : True
    },
]

global task_id_counter
task_id_counter = 4 

@app.route('/tasks', methods=['GET', 'POST'])
def taskss():
    if request.method == "POST":
        global task_id_counter
        title = request.json
        if not bool(title):
            return f"ERROR" , 400
        
        new_todo = {
            "id" : task_id_counter,
            "title" : title["title"],
            "completed" : False
        }
        
        task_id_counter += 1
        tasks.append(new_todo)
        return jsonify({
            "success" : True,
            "all tasks" : new_todo
        }), 200
        
        
    if request.method == "GET":
        return jsonify(tasks)

@app.route('/tasks/<id>', methods=["GET", "PUT", "DELETE"])
def getbyid(id):
    
    if request.method == "GET":
        success = False
        for task in tasks:
            if  task["id"] == int(id):
                success = True
                return jsonify({
                    "success" : success,
                    "task" : task 
                })
        if success == False:
            return jsonify({
                "error" : "id not found",
                "id to search" : id
            })
            
    if request.method == "PUT":
        data = request.json
        for task in tasks:
            if task["id"] == int(id):
                if "completed" in data:
                    task["completed"] = data["completed"]
                if "title" in data:
                    task["title"] = data["title"] 
                return f"{task} updated"
        
        return f"ERROR", 400
        
    if request.method == "DELETE":
        for ind, task in enumerate(tasks):
            if task["id"] == int(id):
                tasks.pop(ind)
                return f"{id} been deleted"
        
        


if __name__ == "__main__":
    app.run(debug=True)