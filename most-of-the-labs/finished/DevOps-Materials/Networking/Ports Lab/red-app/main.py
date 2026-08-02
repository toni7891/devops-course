import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI App Color \"Red\" Running on PORT 3001"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
