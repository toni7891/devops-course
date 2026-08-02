import { Router, Request, Response, NextFunction } from 'express';

const router = Router();

export interface Item {
  id: number;
  name: string;
  status: 'active' | 'inactive';
  createdAt: string;
}

// In-memory store (enough for a lab)
const items: Item[] = [
  { id: 1, name: 'Item Alpha', status: 'active', createdAt: new Date().toISOString() },
  { id: 2, name: 'Item Beta', status: 'inactive', createdAt: new Date().toISOString() },
];
let nextId = 3;

// GET /api/items
router.get('/', (_req: Request, res: Response) => {
  res.json({ success: true, data: items, total: items.length });
});

// GET /api/items/:id
router.get('/:id', (req: Request, res: Response, next: NextFunction) => {
  const id = parseInt(req.params.id, 10);

  if (isNaN(id)) {
    const err = new Error('Invalid ID format') as Error & { statusCode: number };
    err.statusCode = 400;
    return next(err);
  }

  const item = items.find((i) => i.id === id);
  if (!item) {
    const err = new Error(`Item with id ${id} not found`) as Error & { statusCode: number };
    err.statusCode = 404;
    return next(err);
  }

  res.json({ success: true, data: item });
});

// POST /api/items
router.post('/', (req: Request, res: Response, next: NextFunction) => {
  const { name, status } = req.body as Partial<Item>;

  if (!name || typeof name !== 'string' || name.trim() === '') {
    const err = new Error('Field "name" is required') as Error & { statusCode: number };
    err.statusCode = 400;
    return next(err);
  }

  const newItem: Item = {
    id: nextId++,
    name: name.trim(),
    status: status === 'inactive' ? 'inactive' : 'active',
    createdAt: new Date().toISOString(),
  };

  items.push(newItem);
  res.status(201).json({ success: true, data: newItem });
});

export { router as itemsRouter };
