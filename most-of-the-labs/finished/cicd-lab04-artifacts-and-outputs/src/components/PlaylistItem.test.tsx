import { render, screen, fireEvent } from '@testing-library/react'
import PlaylistItem from './PlaylistItem'
import type { Track } from '../types'

const mockTrack: Track = {
  id: '1',
  title: 'Bohemian Rhapsody',
  artist: 'Queen',
  duration: 354,
}

describe('PlaylistItem', () => {
  it('renders the track title and artist', () => {
    render(<PlaylistItem track={mockTrack} onRemove={() => {}} />)
    expect(screen.getByText('Bohemian Rhapsody')).toBeInTheDocument()
    expect(screen.getByText(/Queen/)).toBeInTheDocument()
  })

  it('renders the formatted duration', () => {
    render(<PlaylistItem track={mockTrack} onRemove={() => {}} />)
    expect(screen.getByText(/5:54/)).toBeInTheDocument()
  })

  it('calls onRemove with the track id when Remove is clicked', () => {
    const onRemove = vi.fn()
    render(<PlaylistItem track={mockTrack} onRemove={onRemove} />)
    fireEvent.click(screen.getByRole('button', { name: /remove/i }))
    expect(onRemove).toHaveBeenCalledWith('1')
  })

  it('renders a Remove button', () => {
    render(<PlaylistItem track={mockTrack} onRemove={() => {}} />)
    expect(screen.getByRole('button', { name: /remove/i })).toBeInTheDocument()
  })
})
