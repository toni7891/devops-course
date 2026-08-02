import { Document, model, Schema } from 'mongoose';

export interface IItem extends Document {
  name: string;
  description?: string;
}

const itemSchema = new Schema<IItem>(
  {
    name: { type: String, required: true, trim: true },
    description: { type: String, trim: true },
  },
  { timestamps: true },
);

export const Item = model<IItem>('Item', itemSchema);
