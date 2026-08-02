"""Mongo connect / disconnect. URI defaults to the one built from env."""
import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import config

logger = logging.getLogger("app")

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


async def connect_database(uri: str | None = None) -> AsyncIOMotorDatabase:
    """Connect to MongoDB. Pass an explicit uri to override the env-built one
    (used by tests with a local/in-memory server)."""
    global _client, _db
    uri = uri or config.mongo_uri
    print("Connecting to MongoDB...")
    print(f"URI: {uri}")
    _client = AsyncIOMotorClient(uri)
    _db = _client[config.mongo_db]
    await _client.admin.command("ping")
    logger.info(f"MongoDB connected -> {config.mongo_host}/{config.mongo_db}")
    return _db


async def disconnect_database() -> None:
    global _client, _db
    if _client is not None:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB disconnected")


def get_db() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database not connected")
    return _db
