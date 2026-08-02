export interface Track {
  id: string
  title: string
  artist: string
  duration: number // seconds
}

export interface Playlist {
  id: string
  name: string
  tracks: Track[]
}
