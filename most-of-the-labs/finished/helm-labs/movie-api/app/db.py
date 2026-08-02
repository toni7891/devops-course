import os

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/movies")

# A single shared client/database for the app.
client: AsyncIOMotorClient | None = None
db = None


async def connect() -> None:
    """Open the MongoDB connection and stash the database handle."""
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    # The database name is taken from the URI path (".../movies").
    db = client.get_default_database()
    # Force a round-trip so startup fails fast if Mongo is unreachable.
    await client.admin.command("ping")
    print(f"[db] connected to {MONGO_URI}", flush=True)


async def disconnect() -> None:
    if client is not None:
        client.close()


def movies_collection():
    return db["movies"]
