import { useState, useEffect, useCallback } from 'react'
import { fetchProducts, buyProduct } from './api'
import { ProductCard } from './components/ProductCard'
import { Toast } from './components/Toast'
import type { Product } from './types'
import './App.css'

interface ToastState {
  message: string
  type: 'success' | 'error'
}

export default function App() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [buyingId, setBuyingId] = useState<number | null>(null)
  const [toast, setToast] = useState<ToastState | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchProducts()
      setProducts(data)
    } catch {
      setError('Failed to load products. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const handleBuy = async (id: number) => {
    setBuyingId(id)
    try {
      const updated = await buyProduct(id)
      setProducts((prev) => prev.map((p) => (p.id === updated.id ? updated : p)))
      setToast({ message: `Bought ${updated.name} — stock: ${updated.stock}`, type: 'success' })
    } catch {
      setToast({ message: 'Purchase failed. Try again.', type: 'error' })
    } finally {
      setBuyingId(null)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1 className="logo">ShopFlow</h1>
      </header>

      <main className="main">
        {loading && (
          <div className="grid">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="skeleton" />
            ))}
          </div>
        )}

        {error && (
          <div className="error-banner">
            <p>{error}</p>
            <button type="button" onClick={load}>Try Again</button>
          </div>
        )}

        {!loading && !error && (
          <div className="grid">
            {products.map((p) => (
              <ProductCard
                key={p.id}
                product={p}
                onBuy={handleBuy}
                buying={buyingId === p.id}
              />
            ))}
          </div>
        )}
      </main>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onDismiss={() => setToast(null)}
        />
      )}
    </div>
  )
}
