import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import connect, disconnect
from app.routes.movies import router as movies_router

LOG_LEVEL = os.getenv("LOG_LEVEL", "info").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger("movie-api")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("starting up (log level=%s)", LOG_LEVEL)
    await connect()
    yield
    await disconnect()


app = FastAPI(title="Movie API", lifespan=lifespan)


# Health probe — does not touch the database
@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(movies_router)
