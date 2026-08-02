from pymongo import MongoClient
from pymongo.errors import ConfigurationError, InvalidURI, OperationFailure, ServerSelectionTimeoutError

MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"


def diagnose_connection(uri: str) -> None:
    print("Testing connection to MongoDB Atlas...")

    if "<username>" in uri or "<password>" in uri:
        print("ERROR: Connection string still has placeholder text.")
        print("  Replace <username> and <password> with your actual credentials.")
        return

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("SUCCESS: Connected to MongoDB Atlas!")
        print(f"  Available databases: {client.list_database_names()}")
        client.close()

    except OperationFailure as e:
        print("ERROR: Authentication failed.")
        print("  Cause: Wrong username or password in the connection string.")
        print("  Fix: Go to Atlas → Database Access → Edit Password, then update your URI.")
        print(f"  Details: {e}")

    except ServerSelectionTimeoutError as e:
        print("ERROR: Connection timed out.")
        print("  Cause: Your IP address is not whitelisted in Atlas Network Access.")
        print("  Fix: Go to Atlas → Network Access → Add IP Address → Allow from Anywhere.")
        print(f"  Details: {e}")

    except (ConfigurationError, InvalidURI) as e:
        print("ERROR: Invalid connection string format.")
        print("  Cause: The URI has a formatting problem.")
        print("  Fix: Re-copy the string from Atlas → Connect → Connect your application.")
        print(f"  Details: {e}")

    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")


if __name__ == "__main__":
    diagnose_connection(MONGO_URI)
