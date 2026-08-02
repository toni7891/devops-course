import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import App from './App'
import * as api from './api'

vi.mock('./api')

const mockProducts = [
  { id: 1, name: 'Widget', price: '9.99', stock: 10, created_at: '2026-01-01T00:00:00Z' },
  { id: 2, name: 'Gadget', price: '19.99', stock: 0, created_at: '2026-01-01T00:00:00Z' },
]

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows skeleton loaders while fetching', () => {
    vi.mocked(api.fetchProducts).mockReturnValue(new Promise(() => {}))
    render(<App />)
    expect(document.querySelectorAll('.skeleton').length).toBeGreaterThan(0)
  })

  it('renders product cards after load', async () => {
    vi.mocked(api.fetchProducts).mockResolvedValue(mockProducts)
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('Widget')).toBeInTheDocument()
      expect(screen.getByText('Gadget')).toBeInTheDocument()
    })
  })

  it('shows error banner when fetch fails', async () => {
    vi.mocked(api.fetchProducts).mockRejectedValue(new Error('Network error'))
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText(/Failed to load products/)).toBeInTheDocument()
    })
  })

  it('updates product stock after successful buy', async () => {
    vi.mocked(api.fetchProducts).mockResolvedValue(mockProducts)
    vi.mocked(api.buyProduct).mockResolvedValue({
      ...mockProducts[0],
      stock: 9,
    })

    render(<App />)
    await waitFor(() => screen.getByText('Widget'))

    const buyBtns = screen.getAllByRole('button', { name: /buy now/i })
    await userEvent.click(buyBtns[0])

    await waitFor(() => {
      expect(screen.getByText('Low stock: 9')).toBeInTheDocument()
    })
  })

  it('shows error toast when buy fails', async () => {
    vi.mocked(api.fetchProducts).mockResolvedValue(mockProducts)
    vi.mocked(api.buyProduct).mockRejectedValue(new Error('failed'))

    render(<App />)
    await waitFor(() => screen.getByText('Widget'))

    const buyBtns = screen.getAllByRole('button', { name: /buy now/i })
    await userEvent.click(buyBtns[0])

    await waitFor(() => {
      expect(screen.getByText(/Purchase failed/)).toBeInTheDocument()
    })
  })
})
