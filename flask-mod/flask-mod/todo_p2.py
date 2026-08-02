from flask import Flask, jsonify, request , abort
import uuid
from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity, HTTPException, MethodNotAllowed
app = Flask(__name__)


@app.errorhandler(HTTPException)
def handle_type_error(e):
    
    response = e.get_response()
    response = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description
    }).data
    response.content_type = "application/json"
    return response
    
    
@app.errorhandler(MethodNotAllowed)
def handle_type_error(e):
    response = e.get_response()
    
    response = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description
    })
    response.content_type = "application/json"
    return response
    # return jsonify({
    #     "error": str(e.name),
    #     "ERR_CODE" : str(e.code),
    # }), err_id
    
    
tasks = [
    {
        "id" : "1",
        "title" : "Learn Flask",
        "completed" : False
    },
    {
        "id" : "2",
        "title" : "Build API",
        "completed" : False
    },
    {
        "id" : "3",
        "title" : "Test with postman",
        "completed" : True
    },
]

@app.route('/tasks', methods=["GET", "POST"])
def taskss():
    
    if request.method not in ["GET","POST"]:
        abort(405, description="Incorrect method for request!")
        #raise MethodNotAllowed(massage="Incorrect method for request!")
    
    if request.method == "POST":
        
        title = request.json
        
        if title == {}:
            raise BadRequest("the request body most be JSON")
        
        if not isinstance(title, str):
            raise BadRequest("title must be a string")
    
        if not title.strip():
            raise UnprocessableEntity("string cannot be empty or without spaces")

        
        new_todo = {
            "id" : str(uuid.uuid4()),
            "title" : title["title"],
            "completed" : False
        }
        tasks.append(new_todo)
        return jsonify({
            "success" : True,
            "new task" : new_todo
        }), 200
        
        
    if request.method == "GET":
        return jsonify(tasks)
    

@app.route('/tasks/<id>', methods=["GET", "PUT", "DELETE"])
def getbyid(id):
    # if request.method not in ["GET", "PUT", "DELETE"]:
    #     raise MethodNotAllowed(massage="Incorrect method for request!")
    
    if request.method == "GET":
        if not id.strip():
            raise UnprocessableEntity("ID cannot be empty or spaces")  
        
        for task in tasks:
            if  task["id"] == id:
                return jsonify({
                    "success" : "Success",
                    "task" : task 
                })
        raise NotFound("ID provided does not exist in DB")
            
    if request.method == "PUT":
        data = request.json
        if data == {}:
            raise BadRequest("the request body most be JSON")
        title = data["title"]
        state = data["completed"]
        if not isinstance(title, str):
            raise BadRequest("title must be a string")
        
        if not title.strip():
            raise UnprocessableEntity("string cannot be empty or without spaces")
        
        if not isinstance(state, bool):
            raise BadRequest("state of completed must be BOOLean")
        
        if not id.strip():
            raise UnprocessableEntity("ID cannot be empty or spaces")  
            
        for task in tasks:
            if task["id"] == id:
                task["completed"] = data["completed"]
                task["title"] = data["title"] 
                return f"{task} updated"
        
        raise NotFound("ID provided does not exist in DB")
        
    if request.method == "DELETE":
        if not id.strip():
            raise UnprocessableEntity("ID cannot be empty or spaces")
        for ind, task in enumerate(tasks):
            if task["id"] == id:
                tasks.pop(ind)
                return f"{id} been deleted"
        raise NotFound("ID provided does not exist in DB")

if __name__ == "__main__":
    app.run(debug=True)