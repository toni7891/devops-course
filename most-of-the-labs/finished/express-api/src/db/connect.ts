import mongoose from 'mongoose';

export async function connectDB(uri: string): Promise<void> {
  await mongoose.connect(uri, { serverSelectionTimeoutMS: 5000 });
}
