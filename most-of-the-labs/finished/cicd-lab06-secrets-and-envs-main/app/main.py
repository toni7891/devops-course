"""FastAPI app factory + bootstrap. Mirrors src/app.ts + src/server.ts."""
import logging
import time
from collections import defaultdict
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.config import config
from app.database import connect_database, disconnect_database
from app.errors import HttpError
from app.health import router as health_router
from app.users.routes import router as users_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_database()
    logger.info(f"Listening on http://localhost:{config.port} [{config.app_env}]")
    yield
    await disconnect_database()


# Simple fixed-window rate limit on /api: 100 req / 60s per client IP
_WINDOW_MS = 60_000
_LIMIT = 100
_hits: dict[str, list[float]] = defaultdict(list)


def create_app() -> FastAPI:
    app = FastAPI(title="express-app (python port)", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[config.cors_origin],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=512)

    @app.middleware("http")
    async def rate_limit(request: Request, call_next):
        if request.url.path.startswith("/api"):
            now = time.time() * 1000
            ip = request.client.host if request.client else "unknown"
            recent = [t for t in _hits[ip] if now - t < _WINDOW_MS]
            if len(recent) >= _LIMIT:
                return JSONResponse(status_code=429, content={"error": "Too many requests"})
            recent.append(now)
            _hits[ip] = recent
        return await call_next(request)

    @app.exception_handler(HttpError)
    async def http_error_handler(_: Request, exc: HttpError):
        return JSONResponse(status_code=exc.status, content={"error": exc.message})

    app.include_router(health_router)
    app.include_router(users_router)

    # App status: shows whether running in DEV or TEST + the service port
    @app.get("/status")
    async def status():
        return {
            "status": config.app_env,  # 'DEV' or 'TEST'
            "port": config.port,
            "db": config.mongo_db,
        }

    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=config.port, reload=config.is_dev)


if __name__ == "__main__":
    main()
