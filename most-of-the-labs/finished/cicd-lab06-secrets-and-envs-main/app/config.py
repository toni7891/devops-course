"""Env vars + dynamically built Mongo URI.

This is the main thing of the lab: the MongoDB connection string is
NOT hardcoded — it is assembled from individual env vars at runtime.
"""
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def required(key: str, fallback: str | None = None) -> str:
    v = os.environ.get(key, fallback)
    if v is None:
        raise RuntimeError(f"Missing env var: {key}")
    return v


APP_ENV = required("APP_ENV", "DEV").upper()

MONGO_USER = required("MONGO_USER", "admin")
MONGO_PASS = required("MONGO_PASS", "secret")
MONGO_HOST = required("MONGO_HOST", "localhost:27017")
MONGO_DB = required("MONGO_DB", "express-app")

# Build the connection URI dynamically from the parts
MONGO_URI = (
    f"mongodb+srv://{quote_plus(MONGO_USER)}:{quote_plus(MONGO_PASS)}"
    f"@{MONGO_HOST}/{MONGO_DB}?appName=Cluster0"
)


class Config:
    app_env = APP_ENV  # 'DEV' or 'TEST'
    port = int(required("PORT", "3000"))
    log_level = "info"
    cors_origin = "*"

    mongo_user = MONGO_USER
    mongo_host = MONGO_HOST
    mongo_db = MONGO_DB
    mongo_uri = MONGO_URI

    is_dev = APP_ENV == "DEV"
    is_test = APP_ENV == "TEST"


config = Config()
