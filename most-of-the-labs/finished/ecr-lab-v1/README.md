# ecr-lab-v1

A simple Jokes REST API built with Node.js and Express.

## Getting Started

```bash
git clone https://github.com/IITC-College/ecr-lab-v1.git
cd ecr-lab-v1
npm install
npm start
```

Server runs on `http://localhost:3000` by default. Set `PORT` env var to override.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Returns hello message |
| GET | `/jokes` | Returns all jokes |
| GET | `/jokes/random` | Returns a random joke |
| GET | `/jokes/:id` | Returns a joke by ID (1–8) |

## Example Response

```json
{
  "id": 1,
  "setup": "Why don't scientists trust atoms?",
  "punchline": "Because they make up everything!"
}
```