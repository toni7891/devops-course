from fastapi import FastAPI, Header, HTTPException, Depends, status, UploadFile, File, Form, Request, Response, Cookie
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import time

app = FastAPI(title="Curl Lab API", description="Practice API for curl exercises", version="1.0.0")

basic = HTTPBasic()
bearer = HTTPBearer(auto_error=False)

USERS_DB = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
    3: {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"},
}
NEXT_ID = 4

VALID_TOKEN = "lab-token-12345"
BASIC_USER = "admin"
BASIC_PASS = "secret"


class UserCreate(BaseModel):
    name: str
    email: str
    role: str = "user"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


@app.get("/")
def root():
    return {"message": "Curl Lab API", "docs": "/docs", "endpoints_list": "/endpoints"}


@app.get("/endpoints")
def list_endpoints():
    return {
        "GET /": "root info",
        "GET /hello": "simple hello, supports ?name=",
        "GET /headers": "echo request headers",
        "GET /ip": "client IP",
        "GET /users": "list users, supports ?role=",
        "GET /users/{id}": "get user by id",
        "POST /users": "create user (JSON body)",
        "PUT /users/{id}": "replace user",
        "PATCH /users/{id}": "partial update",
        "DELETE /users/{id}": "delete user",
        "POST /form": "form-encoded data",
        "POST /upload": "file upload (multipart)",
        "GET /protected/bearer": "needs Bearer token",
        "GET /protected/basic": "needs Basic auth",
        "GET /status/{code}": "returns given status code",
        "GET /redirect": "302 redirect to /",
        "GET /cookies/set": "set cookie",
        "GET /cookies/read": "read cookie",
        "GET /delay/{seconds}": "sleep then respond",
        "GET /echo": "echo all query params",
    }


@app.get("/hello")
def hello(name: str = "world"):
    return {"greeting": f"hello, {name}"}


@app.get("/headers")
def echo_headers(request: Request):
    return {"headers": dict(request.headers)}


@app.get("/ip")
def client_ip(request: Request):
    return {"ip": request.client.host}


@app.get("/echo")
def echo(request: Request):
    return {"query_params": dict(request.query_params)}


@app.get("/users")
def list_users(role: Optional[str] = None, limit: int = 10):
    users = list(USERS_DB.values())
    if role:
        users = [u for u in users if u["role"] == role]
    return {"count": len(users), "users": users[:limit]}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = USERS_DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    global NEXT_ID
    new_user = {"id": NEXT_ID, **user.model_dump()}
    USERS_DB[NEXT_ID] = new_user
    NEXT_ID += 1
    return new_user


@app.put("/users/{user_id}")
def replace_user(user_id: int, user: UserCreate):
    if user_id not in USERS_DB:
        raise HTTPException(status_code=404, detail="user not found")
    USERS_DB[user_id] = {"id": user_id, **user.model_dump()}
    return USERS_DB[user_id]


@app.patch("/users/{user_id}")
def patch_user(user_id: int, patch: UserUpdate):
    if user_id not in USERS_DB:
        raise HTTPException(status_code=404, detail="user not found")
    data = patch.model_dump(exclude_unset=True)
    USERS_DB[user_id].update(data)
    return USERS_DB[user_id]


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in USERS_DB:
        raise HTTPException(status_code=404, detail="user not found")
    del USERS_DB[user_id]
    return Response(status_code=204)


@app.post("/form")
def form_data(username: str = Form(...), password: str = Form(...)):
    return {"received": {"username": username, "password_len": len(password)}}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "content_type": file.content_type, "size": len(contents)}


@app.get("/protected/bearer")
def protected_bearer(creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer)):
    if not creds or creds.credentials != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="invalid or missing bearer token")
    return {"message": "access granted via bearer", "token": creds.credentials}


@app.get("/protected/basic")
def protected_basic(creds: HTTPBasicCredentials = Depends(basic)):
    ok_user = secrets.compare_digest(creds.username, BASIC_USER)
    ok_pass = secrets.compare_digest(creds.password, BASIC_PASS)
    if not (ok_user and ok_pass):
        raise HTTPException(status_code=401, detail="invalid basic credentials", headers={"WWW-Authenticate": "Basic"})
    return {"message": "access granted via basic", "user": creds.username}


@app.get("/status/{code}")
def custom_status(code: int):
    return JSONResponse(status_code=code, content={"status_code": code})


@app.get("/redirect")
def redirect():
    return RedirectResponse(url="/", status_code=302)


@app.get("/cookies/set")
def set_cookie(response: Response, value: str = "lab-cookie"):
    response.set_cookie(key="lab", value=value)
    return {"set": value}


@app.get("/cookies/read")
def read_cookie(lab: Optional[str] = Cookie(default=None)):
    return {"lab_cookie": lab}


@app.get("/delay/{seconds}")
def delay(seconds: int):
    seconds = min(seconds, 10)
    time.sleep(seconds)
    return {"slept": seconds}
