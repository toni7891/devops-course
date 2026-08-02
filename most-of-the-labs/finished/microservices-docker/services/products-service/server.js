const express = require('express');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(express.json());

const port = parseInt(process.env.PORT, 10) || 3000;
const serviceName = 'products-service';
const mongoUri = process.env.MONGO_URI || 'mongodb://localhost:27017';
const dbName = 'productsdb';

let mongoClient;
let productsCollection;

async function connectMongo() {
  mongoClient = new MongoClient(mongoUri);
  await mongoClient.connect();
  productsCollection = mongoClient.db(dbName).collection('products');
  console.log(`[${serviceName}] connected to mongo at ${mongoUri}`);
}

const asyncRoute = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: serviceName });
});

app.get('/products', asyncRoute(async (req, res) => {
  const products = await productsCollection.find({}).toArray();
  res.json({ service: serviceName, count: products.length, products });
}));

app.post('/products', asyncRoute(async (req, res) => {
  const { name, price, stock } = req.body || {};
  if (!name || typeof price !== 'number') {
    return res.status(400).json({ error: 'name (string) and price (number) are required' });
  }
  const doc = {
    name,
    price,
    stock: typeof stock === 'number' ? stock : 0,
    createdAt: new Date(),
  };
  const result = await productsCollection.insertOne(doc);
  res.status(201).json({ service: serviceName, product: { _id: result.insertedId, ...doc } });
}));

app.post('/products/:id/buy', asyncRoute(async (req, res) => {
  let _id;
  try {
    _id = new ObjectId(req.params.id);
  } catch {
    return res.status(400).json({ error: 'invalid id' });
  }
  const result = await productsCollection.findOneAndUpdate(
    { _id, stock: { $gt: 0 } },
    { $inc: { stock: -1 } },
    { returnDocument: 'after' }
  );
  if (!result) {
    return res.status(409).json({ service: serviceName, error: 'out of stock or not found' });
  }
  res.json({ service: serviceName, product: result });
}));

app.delete('/products/:id', asyncRoute(async (req, res) => {
  let _id;
  try {
    _id = new ObjectId(req.params.id);
  } catch {
    return res.status(400).json({ error: 'invalid id' });
  }
  const result = await productsCollection.deleteOne({ _id });
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
