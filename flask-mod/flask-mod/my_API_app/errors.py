
from flask import jsonify, Blueprint
from werkzeug.exceptions import HTTPException, MethodNotAllowed, NotFound

errors_bp = Blueprint("errors", __name__)

@errors_bp.app_errorhandler(HTTPException)
def handle_type_error(e):
    custom_message = e.description 
    if e.code == 400:
        custom_message = "bad request use correct json format and str in title"
    elif e.code == 422:
        custom_message = "invalid input of data"

        
    return jsonify({
        "code": e.code,
        "description": e.description,
        "massage" : custom_message
    }), e.code
        
    
@errors_bp.app_errorhandler(MethodNotAllowed)
def handle_type_error1(e):
    response = jsonify({
        "code": 405,
        "name": "Method not allowed for this endpoint of the URL",
        "description": str(e),
    })
    return response, 405

@errors_bp.app_errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({
        "ERROR": "404 Not Found: missing not found",
    }), 404