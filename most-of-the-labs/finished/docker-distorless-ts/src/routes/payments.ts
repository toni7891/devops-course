import express, { Request, Response } from 'express';
import crypto from 'crypto';
import payments, { Payment } from '../store';

const router = express.Router();

interface CreatePaymentBody {
  amount?: unknown;
  currency?: string;
  card?: unknown;
}

// Create payment
router.post('/', (req: Request, res: Response) => {
  const { amount, currency = 'USD', card } = (req.body || {}) as CreatePaymentBody;

  if (typeof amount !== 'number' || amount <= 0) {
    return res.status(400).json({ error: 'amount must be a positive number' });
  }
  if (!card || typeof card !== 'string' || card.length < 12) {
    return res.status(400).json({ error: 'card is required (>=12 chars)' });
  }

  // Dummy logic: card ending in odd digit = declined.
  const lastDigit = Number(card.replace(/\D/g, '').slice(-1));
  const approved = lastDigit % 2 === 0;

  const payment: Payment = {
    id: crypto.randomUUID(),
    amount,
    currency,
    cardLast4: card.slice(-4),
    status: approved ? 'approved' : 'declined',
    refunded: false,
    createdAt: new Date().toISOString(),
  };

  payments.set(payment.id, payment);
  res.status(201).json(payment);
});

// List payments
router.get('/', (_req: Request, res: Response) => {
  res.json([...payments.values()]);
});

// Get payment status
router.get('/:id', (req: Request, res: Response) => {
  const payment = payments.get(req.params.id);
  if (!payment) {
    return res.status(404).json({ error: 'Payment not found' });
  }
  res.json(payment);
});

// Refund payment
router.post('/:id/refund', (req: Request, res: Response) => {
  const payment = payments.get(req.params.id);
  if (!payment) {
    return res.status(404).json({ error: 'Payment not found' });
  }
  if (payment.status !== 'approved') {
    return res.status(409).json({ error: 'Only approved payments can be refunded' });
  }
  if (payment.refunded) {
    return res.status(409).json({ error: 'Payment already refunded' });
  }

  payment.refunded = true;
  payment.status = 'refunded';
  payment.refundedAt = new Date().toISOString();
  res.json(payment);
});

export default router;
