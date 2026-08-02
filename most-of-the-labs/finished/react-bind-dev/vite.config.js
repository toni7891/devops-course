import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    // Bind mount on Windows/Docker: native FS events don't cross the mount.
    // Polling makes HMR detect host file changes inside the container.
    watch: {
      usePolling: true,
      interval: 100,
    },
  },
})
