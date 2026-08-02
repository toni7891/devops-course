from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()
mongo_connection_string = os.getenv("MONGO_URI")
cr = certifi.where()
client = MongoClient(mongo_connection_string, tlsCAFile=cr, serverSelectionTimeoutMS=2000)
db = client['app_todo']
todos_collection = db['data']

def init_db(app):
    global _client, _db
    _client = client
    _db = db
    app.config["DB"] = _db
    
def get_collection(name):
    return _db[name]