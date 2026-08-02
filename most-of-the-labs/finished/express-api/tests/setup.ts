import mongoose from 'mongoose';
import { connectDB } from '../src/db/connect.js';

beforeAll(async () => {
  const uri = process.env.MONGODB_URI;
  if (!uri) throw new Error('MONGODB_URI must be set for tests');
  await connectDB(uri);
});

afterAll(async () => {
  await mongoose.disconnect();
});

afterEach(async () => {
  const { collections } = mongoose.connection;
  for (const key in collections) {
    await collections[key].deleteMany({});
  }
});
