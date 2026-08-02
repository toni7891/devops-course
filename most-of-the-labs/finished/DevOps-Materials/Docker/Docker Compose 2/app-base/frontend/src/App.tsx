import { useEffect, useState } from 'react';

interface Todo {
  id: number;
  text: string;
}

export default function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [text, setText] = useState('');

  useEffect(() => {
    fetch('/api/todos')
      .then(r => r.json())
      .then((data: Todo[]) => setTodos(data))
      .catch(() => setTodos([]));
  }, []);

  async function addTodo(e: React.FormEvent) {
    e.preventDefault();
    if (!text.trim()) return;
    const res = await fetch('/api/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const todo: Todo = await res.json();
    setTodos([...todos, todo]);
    setText('');
  }

  async function removeTodo(id: number) {
    await fetch(`/api/todos/${id}`, { method: 'DELETE' });
    setTodos(todos.filter(t => t.id !== id));
  }

  return (
    <div className="app">
      <h1>Todo App</h1>
      <form onSubmit={addTodo}>
        <input
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="What needs doing?"
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {todos.map(t => (
          <li key={t.id}>
            <span>{t.text}</span>
            <button onClick={() => removeTodo(t.id)}>x</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
