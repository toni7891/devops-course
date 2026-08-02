"""Business rules. Mirrors src/modules/users/user.service.ts."""
from app.errors import HttpError
from app.users import store


async def list_users() -> list[dict]:
    return await store.list_users()


async def get_user(id: str) -> dict:
    user = await store.get_user(id)
    if not user:
        raise HttpError.not_found(f"User {id} not found")
    return user


async def create_user(data: dict) -> dict:
    if await store.find_by_email(data["email"]):
        raise HttpError.conflict(f"Email {data['email']} already in use")
    return await store.create_user(data["name"], data["email"])


async def update_user(id: str, patch: dict) -> dict | None:
    await get_user(id)
    if patch.get("email"):
        existing = await store.find_by_email(patch["email"])
        if existing and existing["id"] != id:
            raise HttpError.conflict("Email already in use")
    return await store.update_user(id, patch)


async def remove_user(id: str) -> None:
    await get_user(id)
    await store.delete_user(id)
