import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import { ProductCard } from './ProductCard'
import type { Product } from '../types'

const product: Product = {
  id: 1,
  name: 'Widget',
  price: '9.99',
  stock: 10,
  created_at: new Date().toISOString(),
}

describe('ProductCard', () => {
  it('renders product name and price', () => {
    render(<ProductCard product={product} onBuy={vi.fn()} buying={false} />)

    expect(screen.getByText('Widget')).toBeInTheDocument()
    expect(screen.getByText('$9.99')).toBeInTheDocument()
  })

  it('shows in stock badge when stock > 10', () => {
    render(<ProductCard product={product} onBuy={vi.fn()} buying={false} />)
    expect(screen.getByText('In stock: 10')).toBeInTheDocument()
  })

  it('shows low stock badge when stock 1-9', () => {
    const low = { ...product, stock: 3 }
    render(<ProductCard product={low} onBuy={vi.fn()} buying={false} />)
    expect(screen.getByText('Low stock: 3')).toBeInTheDocument()
  })

  it('shows out of stock and disables button when stock is 0', () => {
    const out = { ...product, stock: 0 }
    render(<ProductCard product={out} onBuy={vi.fn()} buying={false} />)

    expect(screen.getByText('Out of stock')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /buy now/i })).toBeDisabled()
  })

  it('calls onBuy with product id when clicked', async () => {
    const onBuy = vi.fn()
    render(<ProductCard product={product} onBuy={onBuy} buying={false} />)

    await userEvent.click(screen.getByRole('button', { name: /buy now/i }))
    expect(onBuy).toHaveBeenCalledWith(1)
  })

  it('shows Processing and disables button while buying', () => {
    render(<ProductCard product={product} onBuy={vi.fn()} buying={true} />)

    const btn = screen.getByRole('button', { name: /processing/i })
    expect(btn).toBeDisabled()
  })
})
