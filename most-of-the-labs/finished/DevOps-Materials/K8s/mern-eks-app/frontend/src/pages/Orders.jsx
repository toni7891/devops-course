import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const STATUS_OPTIONS = ['pending', 'in-progress', 'done'];

function apiFetch(url, options = {}) {
  const token = localStorage.getItem('token');
  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers
    }
  });
}

export default function Orders() {
  const [orders,      setOrders]      = useState([]);
  const [title,       setTitle]       = useState('');
  const [description, setDescription] = useState('');
  const navigate = useNavigate();
  const email    = localStorage.getItem('email');

  useEffect(() => {
    loadOrders();
  }, []);

  async function loadOrders() {
    const res = await apiFetch('/api/orders');
    if (res.status === 401) { logout(); return; }
    const data = await res.json();
    setOrders(data);
  }

  async function createOrder(e) {
    e.preventDefault();
    if (!title.trim()) return;
    const res = await apiFetch('/api/orders', {
      method: 'POST',
      body: JSON.stringify({ title, description })
    });
    if (res.ok) {
      setTitle('');
      setDescription('');
      loadOrders();
    }
  }

  async function updateStatus(id, status) {
    await apiFetch(`/api/orders/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ status })
    });
    loadOrders();
  }

  async function deleteOrder(id) {
    if (!window.confirm('Delete this order?')) return;
    await apiFetch(`/api/orders/${id}`, { method: 'DELETE' });
    loadOrders();
  }

  function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    navigate('/login');
  }

  return (
    <div className="orders-container">
      <header className="orders-header">
        <h1>Order Manager</h1>
        <span>{email} — <button onClick={logout} className="logout-btn">Logout</button></span>
      </header>

      <form onSubmit={createOrder} className="create-form">
        <input
          placeholder="Order title *"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <input
          placeholder="Description (optional)"
          value={description}
          onChange={e => setDescription(e.target.value)}
        />
        <button type="submit">Add Order</button>
      </form>

      {orders.length === 0 ? (
        <p className="empty">No orders yet. Create one above.</p>
      ) : (
        <table className="orders-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Description</th>
              <th>Status</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(order => (
              <tr key={order._id}>
                <td>{order.title}</td>
                <td>{order.description}</td>
                <td>
                  <span className={`badge badge-${order.status}`}>
                    {order.status}
                  </span>
                </td>
                <td>{new Date(order.createdAt).toLocaleDateString()}</td>
                <td>
                  <select
                    value={order.status}
                    onChange={e => updateStatus(order._id, e.target.value)}
                  >
                    {STATUS_OPTIONS.map(s => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                  <button
                    onClick={() => deleteOrder(order._id)}
                    className="delete-btn"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
