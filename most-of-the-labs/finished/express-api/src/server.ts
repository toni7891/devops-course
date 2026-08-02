import { config } from './config/env.js';
import { connectDB } from './db/connect.js';
import app from './app.js';

if (!config.mongoUri) {
  console.error('MONGODB_URI environment variable is required');
  process.exit(1);
}

connectDB(config.mongoUri)
  .then(() => {
    app.listen(config.port, () => {
      console.log(`student-api listening on port ${config.port}`);
    });
  })
  .catch((err: Error) => {
    console.error('Failed to connect to MongoDB:', err.message);
    process.exit(1);
  });
