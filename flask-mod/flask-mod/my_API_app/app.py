from flask import Flask, render_template
from routes import tasks_bp
from errors import errors_bp
from database import init_db

app = Flask(__name__)
init_db(app)


app.register_blueprint(tasks_bp)
app.register_blueprint(errors_bp)

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)