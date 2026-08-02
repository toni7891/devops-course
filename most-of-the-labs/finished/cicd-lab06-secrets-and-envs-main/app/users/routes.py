"""User endpoints. Mirrors src/modules/users/user.routes.ts."""
import re

from fastapi import APIRouter, Response

from app.errors import HttpError
from app.schemas import CreateUser, UpdateUser
from app.users import service

router = APIRouter(prefix="/api/users", tags=["users"])

_ID_RE = re.compile(r"^[a-f\d]{24}$", re.IGNORECASE)


def _check_id(id: str) -> None:
    if not _ID_RE.match(id):
        raise HttpError.bad_request("Invalid id")


@router.get("")
async def list_users():
    return await service.list_users()


@router.post("", status_code=201)
async def create_user(body: CreateUser):
    return await service.create_user(body.model_dump())


@router.get("/{id}")
async def get_user(id: str):
    _check_id(id)
    return await service.get_user(id)


@router.patch("/{id}")
async def update_user(id: str, body: UpdateUser):
    _check_id(id)
    return await service.update_user(id, body.model_dump(exclude_none=True))


@router.delete("/{id}", status_code=204)
async def remove_user(id: str):
    _check_id(id)
    await service.remove_user(id)
    return Response(status_code=204)
