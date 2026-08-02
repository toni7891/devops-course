from pymongo import MongoClient

# Replace with your connection string from Atlas
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("Connected to MongoDB Atlas!")
    print(f"Databases: {client.list_database_names()}")
except Exception as e:
    print(f"Connection failed: {e}")
finally:
    client.close()
