import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI App Color \"Blue\" Running on PORT 3000"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
