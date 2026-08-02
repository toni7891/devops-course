from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, status

from app.db import movies_collection
from app.models import MovieIn, MovieOut, serialize

router = APIRouter(prefix="/movies", tags=["movies"])


# GET /movies — list all
@router.get("", response_model=list[MovieOut])
async def list_movies():
    docs = await movies_collection().find().sort("_id", -1).to_list(length=1000)
    return [serialize(d) for d in docs]


# POST /movies — create
@router.post("", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
async def create_movie(movie: MovieIn):
    result = await movies_collection().insert_one(movie.model_dump())
    doc = await movies_collection().find_one({"_id": result.inserted_id})
    return serialize(doc)


# DELETE /movies/{movie_id} — delete by id
@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: str):
    try:
        oid = ObjectId(movie_id)
    except InvalidId:
        raise HTTPException(status_code=404, detail="not found")
    result = await movies_collection().delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="not found")
    return None
