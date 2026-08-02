# HTTP — The Protocol Behind APIs

**Time:** 10:15–11:00

## Topics

### Request

```
Method   URL  HTTP Version
  ↓        ↓      ↓
GET  /users  HTTP/1.1
Host: jsonplaceholder.typicode.com
Accept: application/json
```

| Part | Role | Example |
|------|------|---------|
| Method | What do I want to do | GET, POST, PUT, DELETE |
| URL | On what resource | /users, /posts/1 |
| Headers | Metadata | Content-Type, Authorization |
| Body | Data I'm sending | JSON (mainly in POST/PUT) |

---

### Response

```
HTTP/1.1 200 OK
Content-Type: application/json

{ "id": 1, "name": "Leanne Graham" }
```

| Part | Role | Example |
|------|------|---------|
| Status Code | Success / failure signal | 200, 404, 500 |
| Headers | Metadata | Content-Type |
| Body | Returned data | JSON |

---

### Status Codes — Must Know

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Everything worked |
| 201 | Created | New resource was created |
| 400 | Bad Request | Our request was malformed |
| 401 | Unauthorized | No permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Problem is on the server |

---

## Live Demo with Postman

**Step 1:** Open Postman

**Step 2:** Send GET request:
```
GET https://jsonplaceholder.typicode.com/users
```

**Show students:**
- Status code: 200
- Headers tab in the response
- Body tab — formatted JSON

**Ask the class:**
- How many users are there?
- What is the Content-Type?

---

## Class Exercise — Postman

**Endpoint:**
```
https://jsonplaceholder.typicode.com/users
```

**Tasks:**
1. Send a GET request
2. Find the status code
3. How many users are in the response?
4. What fields does each user have?
5. What is the email of the first user?

**Bonus:** Try sending to `/users/999` — what did you get?
