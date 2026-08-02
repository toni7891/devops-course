# What Is an API?

**Time:** 09:30–10:15

## Objectives

- Shift students from "code only" thinking to systems thinking
- Understand that software is a system of systems

---

## Topics

### 1. What is an API?

API = Application Programming Interface

**Simple definition:** A contract between systems.
One system says: "Send me a request in this format — I'll return a response in this format."

**Analogy: Restaurant**
- You = Client
- Menu = API Contract
- Waiter = API
- Kitchen = Server

---

### 2. Client vs Server

| Client | Server |
|--------|--------|
| Sends requests | Receives and processes |
| Your browser | Website in the cloud |
| The app | The backend |
| Python script | JSONPlaceholder |

---

### 3. Real-World Examples

- Weather app ↔ data server
- Google Maps in Waze ↔ Google API
- Frontend ↔ our Backend
- Python script ↔ JSONPlaceholder

---

### 4. What is REST? (Concept only)

REST = Representational State Transfer

**3 principles that are enough for today:**
1. Runs over HTTP
2. Every resource has a URL: `/users`, `/posts/1`
3. Actions are defined: GET / POST / PUT / DELETE

---

## Mini Exercise — No Code!

Give students:

**Endpoint:**
```
GET https://jsonplaceholder.typicode.com/posts/1
```

**Response:**
```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati",
  "body": "quia et suscipit..."
}
```

**Questions:**
1. Who is the Client in this scenario?
2. Who is the Server?
3. What resource did we request?
4. What data came back?
5. If we wanted all posts — what would the URL look like?

**Expected answers:**
- Client: us (browser / our code)
- Server: jsonplaceholder.typicode.com
- Resource: post #1
- URL for all: `/posts`
