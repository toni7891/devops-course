import express, { Request, Response } from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

interface Todo {
  id: number;
  text: string;
}

let todos: Todo[] = [];
let nextId = 1;

app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok' });
});

app.get('/api/todos', (_req: Request, res: Response) => {
  res.json(todos);
});

app.post('/api/todos', (req: Request, res: Response) => {
  const text = ((req.body?.text as string) || '').trim();
  if (!text) {
    res.status(400).json({ error: 'text required' });
    return;
  }
  const todo: Todo = { id: nextId++, text };
  todos.push(todo);
  res.status(201).json(todo);
});

app.delete('/api/todos/:id', (req: Request, res: Response) => {
  const id = Number(req.params.id);
  todos = todos.filter(t => t.id !== id);
  res.status(204).end();
});

const PORT = 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`backend listening on http://0.0.0.0:${PORT}`);
});
