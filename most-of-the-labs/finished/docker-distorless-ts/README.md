# Dummy Payment System

Basic Express payment API. In-memory store, no real processing. Dummy/teaching use only.

## Run

```bash
npm install
npm start        # or: npm run dev  (auto-reload)
```

Server: http://localhost:3000

## Endpoints

| Method | Path                   | Description            |
|--------|------------------------|------------------------|
| GET    | `/health`              | Health check           |
| POST   | `/payments`            | Create payment         |
| GET    | `/payments`            | List all payments      |
| GET    | `/payments/:id`        | Get payment status     |
| POST   | `/payments/:id/refund` | Refund a payment       |

## Dummy rule

Card number ending in **even** digit → `approved`. Odd → `declined`.

## Examples

Create (approved — ends in 2):

```bash
curl -X POST http://localhost:3000/payments \
  -H "Content-Type: application/json" \
  -d '{"amount": 49.99, "currency": "USD", "card": "4242424242424242"}'
```

Get status:

```bash
curl http://localhost:3000/payments/<id>
```

Refund:

```bash
curl -X POST http://localhost:3000/payments/<id>/refund
```
