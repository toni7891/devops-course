const express = require('express');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(express.json());

const port = parseInt(process.env.PORT, 10) || 3000;
const serviceName = 'users-service';
const mongoUri = process.env.MONGO_URI || 'mongodb://localhost:27017';
const dbName = 'usersdb';

let mongoClient;
let usersCollection;

async function connectMongo() {
  mongoClient = new MongoClient(mongoUri);
  await mongoClient.connect();
  usersCollection = mongoClient.db(dbName).collection('users');
  console.log(`[${serviceName}] connected to mongo at ${mongoUri}`);
}

const asyncRoute = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: serviceName });
});

app.get('/users', asyncRoute(async (req, res) => {
  const users = await usersCollection.find({}).toArray();
  res.json({ service: serviceName, count: users.length, users });
}));

app.post('/users', asyncRoute(async (req, res) => {
  const { name, email } = req.body || {};
  if (!name || !email) {
    return res.status(400).json({ error: 'name and email are required' });
  }
  const doc = { name, email, createdAt: new Date() };
  const result = await usersCollection.insertOne(doc);
  res.status(201).json({ service: serviceName, user: { _id: result.insertedId, ...doc } });
}));

app.delete('/users/:id', asyncRoute(async (req, res) => {
  let _id;
  try {
    _id = new ObjectId(req.params.id);
  } catch {
    return res.status(400).json({ error: 'invalid id' });
  }
  const result = await usersCollection.deleteOne({ _id });
  if (result.deletedCount === 0) {
    return res.status(404).json({ service: serviceName, error: 'not found' });
  }
  res.json({ service: serviceName, deleted: result.deletedCount });
}));

app.use((err, req, res, next) => {
  console.error(`[${serviceName}] request failed:`, err);
  res.status(500).json({ service: serviceName, error: 'internal error' });
});

async function start() {
  for (let attempt = 1; attempt <= 10; attempt++) {
    try {
      await connectMongo();
      break;
    } catch (err) {
      console.log(`[${serviceName}] mongo not ready (attempt ${attempt}): ${err.message}`);
      if (attempt === 10) {
        console.error(`[${serviceName}] giving up after ${attempt} attempts`);
        process.exit(1);
      }
      await new Promise((r) => setTimeout(r, 2000));
    }
  }

  const server = app.listen(port, () => {
    console.log(`[${serviceName}] listening on :${port}`);
  });

  const shutdown = async (signal) => {
    console.log(`[${serviceName}] ${signal} received, shutting down`);
    server.close(() => console.log(`[${serviceName}] http closed`));
    if (mongoClient) await mongoClient.close();
    process.exit(0);
  };
  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));
}

start();
