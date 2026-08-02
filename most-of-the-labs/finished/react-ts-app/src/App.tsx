import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <main style={{ fontFamily: 'system-ui', padding: '2rem' }}>
      <h1>react-ts-app</h1>
      <p>React + TypeScript + Vite, served from a distroless image.</p>
      <button onClick={() => setCount((c) => c + 1)}>count is {count}</button>
    </main>
  )
}

export default App
