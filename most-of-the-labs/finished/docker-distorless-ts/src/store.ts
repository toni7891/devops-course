export interface Payment {
  id: string;
  amount: number;
  currency: string;
  cardLast4: string;
  status: 'approved' | 'declined' | 'refunded';
  refunded: boolean;
  createdAt: string;
  refundedAt?: string;
}

// In-memory payment store. Dummy only — resets on restart.
const payments = new Map<string, Payment>();

export default payments;
