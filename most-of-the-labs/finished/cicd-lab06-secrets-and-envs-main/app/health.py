"""Health endpoints. Mirrors src/routes/health.routes.ts."""
import time

from fastapi import APIRouter

router = APIRouter(tags=["health"])
_started_at = time.time()


@router.get("/livez")
async def livez():
    return {"status": "ok"}


@router.get("/readyz")
async def readyz():
    return {"status": "ready", "uptimeMs": int((time.time() - _started_at) * 1000)}
