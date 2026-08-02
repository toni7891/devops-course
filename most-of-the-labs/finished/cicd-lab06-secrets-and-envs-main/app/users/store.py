"""Mongo data access for users. Mirrors src/modules/users/user.store.ts."""
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from app.database import get_db

COLLECTION = "users"


def _to_user(doc: dict | None) -> dict | None:
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "createdAt": doc["createdAt"],
    }


def _oid(id: str) -> ObjectId | None:
    try:
        return ObjectId(id)
    except (InvalidId, TypeError):
        return None


async def list_users() -> list[dict]:
    cursor = get_db()[COLLECTION].find()
    return [_to_user(d) for d in await cursor.to_list(length=None)]


async def get_user(id: str) -> dict | None:
    oid = _oid(id)
    if oid is None:
        return None
    return _to_user(await get_db()[COLLECTION].find_one({"_id": oid}))


async def find_by_email(email: str) -> dict | None:
    return _to_user(await get_db()[COLLECTION].find_one({"email": email}))


async def create_user(name: str, email: str) -> dict:
    doc = {"name": name, "email": email, "createdAt": datetime.now(timezone.utc).isoformat()}
    res = await get_db()[COLLECTION].insert_one(doc)
    doc["_id"] = res.inserted_id
    return _to_user(doc)


async def update_user(id: str, patch: dict) -> dict | None:
    oid = _oid(id)
    if oid is None:
        return None
    doc = await get_db()[COLLECTION].find_one_and_update(
        {"_id": oid}, {"$set": patch}, return_document=True
    )
    return _to_user(doc)


async def delete_user(id: str) -> bool:
    oid = _oid(id)
    if oid is None:
        return False
    res = await get_db()[COLLECTION].delete_one({"_id": oid})
    return res.deleted_count > 0


async def reset() -> None:
    await get_db()[COLLECTION].delete_many({})
