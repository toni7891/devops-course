from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app.routes import tasks_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(tasks_bp)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": {"message": "Resource not found", "code": "NOT_FOUND"}
        }), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return jsonify({
                "success": False,
                "error": {"message": error.description, "code": str(error.code)}
            }), error.code
        return jsonify({
            "success": False,
            "error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}
        }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
