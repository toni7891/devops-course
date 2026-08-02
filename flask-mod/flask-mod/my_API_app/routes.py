from flask import jsonify, request, Blueprint
from werkzeug.exceptions import MethodNotAllowed
from models import (
    getall, getby_id, post_new, edit_one, delete_one,
    get_collections, create_collection, delete_collection,
    get_tasks_for_collection, post_new_to_collection
)

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route('/collections', methods=["GET", "POST"])
def collections():
    if request.method not in ["GET", "POST"]:
        raise MethodNotAllowed("incorrect method for request")
    if request.method == "GET":
        return jsonify(get_collections()), 200
    if request.method == "POST":
        data = request.json
        # prefer 'collection' key, accept legacy 'name'
        collection = (data.get("collection") if data else None) or (data.get("name") if data else None)
        return jsonify(create_collection(collection)), 201


@tasks_bp.route('/collections/<collection>', methods=["DELETE"])
def collection_delete(collection):
    if request.method != "DELETE":
        raise MethodNotAllowed("incorrect method for request")
    return jsonify(delete_collection(collection)), 200


@tasks_bp.route('/tasks/<collection_name>', methods=["GET", "POST"])
def tasks_by_collection(collection_name):
    if request.method not in ["GET", "POST"]:
        raise MethodNotAllowed("incorrect method for request")
    if request.method == "GET":
        return jsonify(get_tasks_for_collection(collection_name)), 200
    if request.method == "POST":
        data_new = request.json
        return jsonify(post_new_to_collection(collection_name, data_new)), 201


@tasks_bp.route('/tasks', methods=["GET", "POST"])
def taskss():
    # Support query param ?collection=NAME
    if request.method not in ["GET","POST"]:
        raise MethodNotAllowed("incorrect method for request")

    if request.method == "POST":
        data_new = request.json or {}
        # Expect caller to include a `collection` field; default to General
        collection_name = data_new.get("collection", "General")
        return jsonify(post_new_to_collection(collection_name, data_new)),201

    if request.method == "GET":
        collection_q = request.args.get("collection")
        if not collection_q or collection_q == "All":
            return jsonify(getall())
        else:
            return jsonify(get_tasks_for_collection(collection_q)), 200


@tasks_bp.route('/tasks/<id>', methods=["GET", "PUT", "DELETE"])
def getbyid(id):    
    if request.method not in ["GET", "PUT", "DELETE"]:
        raise MethodNotAllowed("incorrect method for request")
    
    if request.method == "GET":        
        return jsonify(getby_id(id)),200
            
    if request.method == "PUT":
        return jsonify(edit_one(id)),200
        
    if request.method == "DELETE":
        return jsonify(delete_one(id)),200
