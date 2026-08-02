const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

let todos = [];
let nextId = 1;

app.get('/api/todos', (req, res) => {
  res.json(todos);
});

app.post('/api/todos', (req, res) => {
  const text = (req.body && req.body.text || '').trim();
  if (!text) return res.status(400).json({ error: 'text required' });
  const todo = { id: nextId++, text };
  todos.push(todo);
  res.status(201).json(todo);
});

app.delete('/api/todos/:id', (req, res) => {
  const id = Number(req.params.id);
  todos = todos.filter(t => t.id !== id);
  res.status(204).end();
});

const PORT = 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`backend listening on http://0.0.0.0:${PORT}`);
});
