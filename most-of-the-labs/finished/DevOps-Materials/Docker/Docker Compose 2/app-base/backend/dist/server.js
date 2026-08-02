"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const app = (0, express_1.default)();
app.use((0, cors_1.default)());
app.use(express_1.default.json());
let todos = [];
let nextId = 1;
app.get('/api/todos', (_req, res) => {
    res.json(todos);
});
app.post('/api/todos', (req, res) => {
    const text = (req.body?.text || '').trim();
    if (!text) {
        res.status(400).json({ error: 'text required' });
        return;
    }
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
