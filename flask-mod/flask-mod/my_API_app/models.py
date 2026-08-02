from flask import request
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity
from database import get_collection
from bson.objectid import ObjectId


def getall():
    col = get_collection("data")
    all_todos = list(col.find())
    for task in all_todos:
        task["_id"] = str(task["_id"])
        
    return all_todos 


def get_collections():
    col = get_collection("collections")
    # support existing docs that may use either 'collection' or legacy 'name'
    items = list(col.find({}, {"_id": 0, "collection": 1, "name": 1}))
    return [it.get("collection") or it.get("name") for it in items]


def create_collection(collection):
    if not collection or not isinstance(collection, str) or not collection.strip():
        raise UnprocessableEntity("collection must be a non-empty string")

    collection = collection.strip()
    col = get_collection("collections")
    existing = col.find_one({"$or": [{"collection": collection}, {"name": collection}]})
    if existing:
        raise BadRequest("Collection already exists")
    col.insert_one({"collection": collection})
    return {"success": True, "collection": collection}


def delete_collection(collection_name):
    if not collection_name or not isinstance(collection_name, str):
        raise BadRequest("Invalid collection name")
    col = get_collection("collections")

    res = col.delete_one({"$or": [{"collection": collection_name}, {"name": collection_name}]})

    data_col = get_collection("data")
    data_col.delete_many({"collection": collection_name})
    if res.deleted_count == 0:
        raise NotFound("Collection not found")
    return {"success": True, "deleted": collection_name}


def get_tasks_for_collection(collection_name):
    col = get_collection("data")
    all_todos = list(col.find({"collection": collection_name}))
    for task in all_todos:
        task["_id"] = str(task["_id"])
    return all_todos


def post_new_to_collection(collection_name, data):
    if not data or "title" not in data:
        raise UnprocessableEntity("the request body most be JSON")

    if not isinstance(data["title"], str):
        raise UnprocessableEntity("title must be a string")

    if not data["title"].strip():
        raise UnprocessableEntity("string cannot be empty or without spaces")
    
    if "completed" in data:
        if not isinstance(data["completed"], bool):
            raise BadRequest("The 'completed' field must be a boolean (true/false).")
    
    new_todo = {
        "title" : data.get("title").strip(),
        "completed" : data.get("completed", False),
        "collection": collection_name
    }
    col = get_collection("data")
    col.insert_one(new_todo)
    new_todo["_id"] = str(new_todo["_id"])
    
    return {
        "success" : True,
        "new task" : new_todo
    }


def getby_id(id1): 
    try:
        col = get_collection("data")
        needed_task = col.find_one({"_id": ObjectId(id1)})
        if needed_task:
            needed_task["_id"] = str(needed_task["_id"])
            return needed_task
    except (NotFound, Exception):
        raise NotFound("ID provided does not exist in DB")


def post_new(data):   
    
    if not data or "title" not in data:
        raise UnprocessableEntity("the request body most be JSON")

    if not isinstance(data["title"], str):
        raise UnprocessableEntity("title must be a string")

    if not data["title"].strip():
        raise UnprocessableEntity("string cannot be empty or without spaces")
    
    if "completed" in data:
        if not isinstance(data["completed"], bool):
            raise BadRequest("The 'completed' field must be a boolean (true/false).")
    
    new_todo = {
        "title" : data.get("title").strip(),
        "completed" : data.get("completed", False)
    }
    col = get_collection("data")
    col.insert_one(new_todo)
    new_todo["_id"] = str(new_todo["_id"])
    
    return {
        "success" : True,
        "new task" : new_todo
    }


def edit_one(id):    
    update_data = request.json  
    
    check_id = getby_id(id)
    
    col = get_collection("data")
    if not update_data:
        raise BadRequest("the request body most be JSON")
    
    
    if "title" in update_data:
        if not isinstance(update_data["title"], str):
            raise BadRequest("title must be a string")
        if not update_data["title"].strip():
            raise UnprocessableEntity("string cannot be empty or without spaces")
    
    if "completed" in update_data:
        if not isinstance(update_data["completed"], bool):
            raise BadRequest("state of completed must be boolean") 
    
    
    update_fields = {}
    if "title" in update_data:
        update_fields["title"] = update_data["title"].strip()
    if "completed" in update_data:
        update_fields["completed"] = update_data["completed"]
    
    if not update_fields:
        raise BadRequest("At least one field (title or completed) must be provided for update")
    
    success = col.update_one(
        {"_id": ObjectId(id)},{
            "$set" : update_fields
        })
    
    if success.matched_count == 0:
        raise NotFound("ID provided does not exist in DB")

    
    updated_task = getby_id(id)
    return updated_task        


def delete_one(id):
    try:
        verify_id = getby_id(id)
        col = get_collection("data")
        success = col.delete_one({"_id": ObjectId(id)})
        if success.deleted_count == 0:
                raise NotFound("ID provided does not exist in DB")
        return f"{id} has been deleted"
    except Exception:
        raise NotFound("ID provided does not exist in DB")

