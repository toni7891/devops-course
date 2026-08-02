import { render, screen, fireEvent } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the Harmonic Haven heading', () => {
    render(<App />)
    expect(screen.getByText('Harmonic Haven')).toBeInTheDocument()
  })

  it('renders the initial track list', () => {
    render(<App />)
    expect(screen.getByText('Bohemian Rhapsody')).toBeInTheDocument()
  })

  it('removes a track when its Remove button is clicked', () => {
    render(<App />)
    const removeButtons = screen.getAllByRole('button', { name: /remove/i })
    fireEvent.click(removeButtons[0])
    expect(screen.queryByText('Bohemian Rhapsody')).not.toBeInTheDocument()
  })
})
