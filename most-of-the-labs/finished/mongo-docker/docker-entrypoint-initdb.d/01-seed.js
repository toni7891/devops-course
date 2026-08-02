// Database initialization script — PROVIDED, do not modify.
//
// MongoDB runs every .js / .sh file in /docker-entrypoint-initdb.d/
// ONLY when it starts with an EMPTY data directory (a fresh volume).
//
// Your job is NOT to write this file. Your job is to wire it into your
// image (via the Dockerfile) so MongoDB executes it on first start, then
// prove the seeded data persists across container removal.

const appdb = db.getSiblingDB('appdb');

// --- application DB user ---
// The root user (MONGO_INITDB_ROOT_*) is for admin only. Real apps connect
// with a least-privilege user scoped to their own database. Create one here
// so the backend team connects as `appuser`, not root.
appdb.createUser({
  user: 'appuser',
  pwd: 'appsecret',
  roles: [{ role: 'readWrite', db: 'appdb' }],
});

// --- sample users ---
appdb.users.insertMany([
  { _id: 1, name: 'Alice Cohen',   email: 'alice@example.com', createdAt: new Date() },
  { _id: 2, name: 'Bob Levi',      email: 'bob@example.com',   createdAt: new Date() },
  { _id: 3, name: 'Carol Mizrahi', email: 'carol@example.com', createdAt: new Date() },
]);

// --- products ---
appdb.products.insertMany([
  { _id: 101, name: 'Mechanical Keyboard', price: 349.90, stock: 25 },
  { _id: 102, name: 'USB-C Hub',           price: 129.00, stock: 60 },
  { _id: 103, name: '27" Monitor',         price: 1299.00, stock: 12 },
  { _id: 104, name: 'Webcam 1080p',        price: 219.50, stock: 40 },
]);

// --- orders --- (reference users + products)
appdb.orders.insertMany([
  {
    _id: 1001, userId: 1, status: 'paid', total: 607.90, createdAt: new Date(),
    items: [
      { productId: 101, qty: 1, unitPrice: 349.90 },
      { productId: 102, qty: 2, unitPrice: 129.00 },
    ],
  },
  {
    _id: 1002, userId: 2, status: 'pending', total: 1299.00, createdAt: new Date(),
    items: [{ productId: 103, qty: 1, unitPrice: 1299.00 }],
  },
  {
    _id: 1003, userId: 3, status: 'shipped', total: 348.50, createdAt: new Date(),
    items: [
      { productId: 104, qty: 1, unitPrice: 219.50 },
      { productId: 102, qty: 1, unitPrice: 129.00 },
    ],
  },
]);

// --- confirm seed (visible in `docker logs <container>`) ---
print('Seed complete for appdb:');
print('  users:    ' + appdb.users.countDocuments());
print('  products: ' + appdb.products.countDocuments());
print('  orders:   ' + appdb.orders.countDocuments());
