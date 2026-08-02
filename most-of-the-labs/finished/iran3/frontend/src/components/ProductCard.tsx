import type { Product } from '../types'

const EMOJIS = ['🖥️', '🖱️', '⌨️', '🔌', '💾', '📱', '🎧', '🖨️']

interface Props {
  product: Product
  onBuy: (id: number) => void
  buying: boolean
}

export function ProductCard({ product, onBuy, buying }: Props) {
  const outOfStock = product.stock === 0
  const lowStock = product.stock > 0 && product.stock < 10
  const emoji = EMOJIS[product.id % EMOJIS.length]

  return (
    <div className="product-card">
      <div className="product-emoji">{emoji}</div>
      <h3 className="product-name">{product.name}</h3>
      <div className="product-price">${Number(product.price).toFixed(2)}</div>
      <div className={`stock-badge ${outOfStock ? 'out' : lowStock ? 'low' : 'in'}`}>
        {outOfStock ? 'Out of stock' : lowStock ? `Low stock: ${product.stock}` : `In stock: ${product.stock}`}
      </div>
      <button
        className="buy-btn"
        disabled={outOfStock || buying}
        onClick={() => onBuy(product.id)}
      >
        {buying ? 'Processing...' : 'BUY NOW'}
      </button>
    </div>
  )
}
