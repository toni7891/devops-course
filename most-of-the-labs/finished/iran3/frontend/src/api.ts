import type { Product } from './types'

export async function fetchProducts(): Promise<Product[]> {
  const res = await fetch('/api/products')
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function buyProduct(id: number): Promise<Product> {
  const res = await fetch(`/api/products/${id}/stock`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ delta: -1 }),
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}
