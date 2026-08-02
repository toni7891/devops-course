from pydantic import BaseModel


class MovieIn(BaseModel):
    title: str
    year: int | None = None
    genre: str | None = None


class MovieOut(MovieIn):
    id: str


def serialize(doc: dict) -> dict:
    """Turn a Mongo document into a JSON-friendly dict (ObjectId -> str)."""
    return {
        "id": str(doc["_id"]),
        "title": doc.get("title"),
        "year": doc.get("year"),
        "genre": doc.get("genre"),
    }
