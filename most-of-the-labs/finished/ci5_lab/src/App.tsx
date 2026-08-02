import { useState } from 'react'
import type { Track } from './types'
import PlaylistItem from './components/PlaylistItem'

const INITIAL_TRACKS: Track[] = [
  { id: '1', title: 'Bohemian Rhapsody', artist: 'Queen', duration: 354 },
  { id: '2', title: 'Hotel California', artist: 'Eagles', duration: 391 },
  { id: '3', title: 'Stairway to Heaven', artist: 'Led Zeppelin', duration: 482 },
]

export default function App() {
  const [tracks, setTracks] = useState<Track[]>(INITIAL_TRACKS)

  const handleRemove = (id: string) => {
    setTracks(prev => prev.filter(track => track.id !== id))
  }

  return (
    <div>
      <h1>Harmonic Haven</h1>
      {tracks.length === 0 ? (
        <p>No tracks in playlist</p>
      ) : (
        <ul>
          {tracks.map(track => (
            <PlaylistItem key={track.id} track={track} onRemove={handleRemove} />
          ))}
        </ul>
      )}
    </div>
  )
}
