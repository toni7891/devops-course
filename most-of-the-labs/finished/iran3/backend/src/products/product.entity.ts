export interface Product {
  id: number;
  name: string;
  price: string; // NUMERIC comes back as string from pg
  stock: number;
  created_at: Date;
}
