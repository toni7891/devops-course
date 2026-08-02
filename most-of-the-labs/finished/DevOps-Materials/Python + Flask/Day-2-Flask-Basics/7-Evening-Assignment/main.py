from flask import Flask

from app.routes import tasks_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(tasks_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
