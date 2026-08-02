# Curl Lab API

Small FastAPI app for practicing `curl`. Clone, run locally, hit endpoints.

## Setup

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
fastapi dev main.py
```

API runs at `http://localhost:8000`. Swagger docs at `/docs`.

## Endpoint Map

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | root info |
| GET | `/endpoints` | list all endpoints |
| GET | `/hello?name=X` | greeting (query param) |
| GET | `/headers` | echo request headers |
| GET | `/ip` | client IP |
| GET | `/echo?...` | echo query params |
| GET | `/users?role=&limit=` | list users |
| GET | `/users/{id}` | get user |
| POST | `/users` | create user (JSON) |
| PUT | `/users/{id}` | replace user |
| PATCH | `/users/{id}` | partial update |
| DELETE | `/users/{id}` | delete user |
| POST | `/form` | form-encoded |
| POST | `/upload` | file upload (multipart) |
| GET | `/protected/bearer` | Bearer auth |
| GET | `/protected/basic` | Basic auth |
| GET | `/status/{code}` | force status code |
| GET | `/redirect` | 302 redirect |
| GET | `/cookies/set?value=` | set cookie |
| GET | `/cookies/read` | read cookie |
| GET | `/delay/{seconds}` | sleep then respond |

## Credentials

- Bearer token: `lab-token-12345`
- Basic auth: `admin` / `secret`

---

## Curl Exercises

### 1. Basic GET

```bash
curl http://localhost:8000/
curl http://localhost:8000/hello
curl "http://localhost:8000/hello?name=Alice"
```

### 2. Verbose output (see headers)

```bash
curl -v http://localhost:8000/hello
```

### 3. Headers only

```bash
curl -I http://localhost:8000/
curl --head http://localhost:8000/
```

### 4. Custom request headers

```bash
curl -H "X-Custom: hello" -H "User-Agent: lab-client" http://localhost:8000/headers
```

### 5. Query params

```bash
curl "http://localhost:8000/echo?foo=1&bar=baz"
curl "http://localhost:8000/users?role=admin&limit=5"
```

### 6. Path params

```bash
curl http://localhost:8000/users/1
curl http://localhost:8000/users/999   # 404
```

### 7. POST JSON

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Dave","email":"dave@example.com","role":"user"}'
```

### 8. POST JSON from file

```bash
echo '{"name":"Eve","email":"eve@example.com"}' > user.json
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d @user.json
```

### 9. PUT (full replace)

```bash
curl -X PUT http://localhost:8000/users/2 \
  -H "Content-Type: application/json" \
  -d '{"name":"Bob Updated","email":"bob2@example.com","role":"admin"}'
```

### 10. PATCH (partial)

```bash
curl -X PATCH http://localhost:8000/users/2 \
  -H "Content-Type: application/json" \
  -d '{"role":"admin"}'
```

### 11. DELETE

```bash
curl -X DELETE -i http://localhost:8000/users/3
```

### 12. Form data (urlencoded)

```bash
curl -X POST http://localhost:8000/form \
  -d "username=alice&password=hunter2"
```

### 13. File upload (multipart)

```bash
echo "hello file" > test.txt
curl -X POST http://localhost:8000/upload \
  -F "file=@test.txt"
```

### 14. Bearer auth

```bash
curl http://localhost:8000/protected/bearer   # 401
curl -H "Authorization: Bearer lab-token-12345" http://localhost:8000/protected/bearer
```

### 15. Basic auth

```bash
curl -u admin:secret http://localhost:8000/protected/basic
curl -u admin:wrong http://localhost:8000/protected/basic   # 401
```

### 16. Status codes

```bash
curl -i http://localhost:8000/status/200
curl -i http://localhost:8000/status/404
curl -i http://localhost:8000/status/500
```

### 17. Follow redirects

```bash
curl -i http://localhost:8000/redirect       # see 302
curl -L http://localhost:8000/redirect       # follow
```

### 18. Cookies

```bash
curl -c cookies.txt "http://localhost:8000/cookies/set?value=lab123"
curl -b cookies.txt http://localhost:8000/cookies/read
```

### 19. Timeout

```bash
curl --max-time 3 http://localhost:8000/delay/5   # times out
curl --max-time 10 http://localhost:8000/delay/2  # ok
```

### 20. Save response to file

```bash
curl -o users.json http://localhost:8000/users
```

### 21. Silent + only HTTP code

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/users/1
```

### 22. Pipe to jq

```bash
curl -s http://localhost:8000/users | jq '.users[].name'
```

---

## Lab Tasks (try yourself)

1. Create 5 new users via POST.
2. List only users with role `admin`.
3. PATCH user 1 to change email.
4. Delete user 2 and confirm with GET (expect 404).
5. Hit `/protected/bearer` with wrong token, then right token.
6. Upload an image file and inspect `size` field.
7. Save cookie from `/cookies/set` and replay it on `/cookies/read`.
8. Force a 500 from `/status/500` and observe response body.
9. Use `-w "%{time_total}\n"` to measure latency on `/delay/2`.
10. Combine: chain `curl` calls in a bash script that creates → fetches → deletes a user.
