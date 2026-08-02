"""Integration tests. No external DB — mongomock-motor in-memory Mongo.

Mirrors tests/users.test.ts.
"""
import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

os.environ["APP_ENV"] = "TEST"

from app import database  # noqa: E402
from app.config import config  # noqa: E402
from app.main import app  # noqa: E402


@pytest_asyncio.fixture(autouse=True)
async def fake_db(monkeypatch):
    client = AsyncMongoMockClient()
    db = client[config.mongo_db]
    monkeypatch.setattr(database, "_client", client)
    monkeypatch.setattr(database, "_db", db)
    await db["users"].delete_many({})
    yield


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_status_reports_test_env(client):
    r = await client.get("/status")
    assert r.status_code == 200
    assert r.json()["status"] == "TEST"


@pytest.mark.asyncio
async def test_health(client):
    assert (await client.get("/livez")).json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_user_crud(client):
    r = await client.post("/api/users", json={"name": "Ada", "email": "ada@x.com"})
    assert r.status_code == 201
    uid = r.json()["id"]

    r = await client.get("/api/users")
    assert len(r.json()) == 1

    r = await client.get(f"/api/users/{uid}")
    assert r.json()["name"] == "Ada"

    r = await client.patch(f"/api/users/{uid}", json={"name": "Ada L."})
    assert r.json()["name"] == "Ada L."

    r = await client.delete(f"/api/users/{uid}")
    assert r.status_code == 204

    assert (await client.get(f"/api/users/{uid}")).status_code == 404


@pytest.mark.asyncio
async def test_duplicate_email_conflicts(client):
    await client.post("/api/users", json={"name": "A", "email": "dup@x.com"})
    r = await client.post("/api/users", json={"name": "B", "email": "dup@x.com"})
    assert r.status_code == 409


@pytest.mark.asyncio
async def test_invalid_id_rejected(client):
    assert (await client.get("/api/users/not-an-id")).status_code == 400
