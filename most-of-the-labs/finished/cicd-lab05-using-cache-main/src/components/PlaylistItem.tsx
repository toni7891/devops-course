import type { Track } from '../types'

function formatDuration(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

interface Props {
  track: Track
  onRemove: (id: string) => void
}

export default function PlaylistItem({ track, onRemove }: Props) {
  return (
    <li>
      <span>{track.title}</span>
      <span> — {track.artist}</span>
      <span> ({formatDuration(track.duration)})</span>
      <button onClick={() => onRemove(track.id)}>Remove</button>
    </li>
  )
}
