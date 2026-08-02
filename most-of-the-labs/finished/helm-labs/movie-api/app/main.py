from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import connect, disconnect
from app.routes.movies import router as movies_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await connect()
    yield
    await disconnect()


app = FastAPI(title="Movie API", lifespan=lifespan)


# Health probe — does not touch the database
@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(movies_router)
