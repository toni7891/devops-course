from flask import Flask, jsonify, request
from datetime import datetime, timezone 
app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({
        "message": "API is running"
    })
    

@app.route('/status')
def status():
    return jsonify({
        "status" : "ok",
        "version" : "1.0.0"
    })
    
    
@app.route('/time')
def cur_time():
    now = datetime.now(timezone.utc)
    
    return jsonify({
        "time" : now
    }) 


@app.route('/info')
def info():    
    return jsonify({
        "app" : "Flask prac",
        "author" : "Tony",
        "day": 2
    })
    
@app.route('/echo', methods=["POST"])
def echo():
    body = request.json 
    
    if not bool(body):
        return jsonify({
            "success" : False,
            "error" : "body not found"
            
        }), 400
    
    return jsonify({
        "success" : True,
        "echo" : body
    }), 200

USERS = [
    {"id": 1 , "name": "bob"},
    {"id": 2 , "name": "gam"},
    {"id": 3 , "name": "bob bam"},
    {"id": 4 , "name": "bim"}
]

@app.route('/search')
def search():
    name = request.args.get("name")
    
    if not name:
        return jsonify({
            "success" : False,
            "error": "name required"
        })
        
    res = []
    for u in USERS:
        if name in u["name"]:
            res.append(u)
            
    return jsonify({
        "success" : True,
        "name" : res                
    })

if __name__ == "__main__":
    app.run(debug=True)
