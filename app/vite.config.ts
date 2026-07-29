import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 3000,
    // Poll for file changes when running in Docker (bind-mounted source).
    watch: {
      usePolling: process.env.CHOKIDAR_USEPOLLING === '1',
    },
  },
})
