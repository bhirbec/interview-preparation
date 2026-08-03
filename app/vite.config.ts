import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // sql.js ships an emscripten CommonJS bundle; pre-bundle it at startup so the
  // first import can't trigger a dependency re-optimization and a full reload.
  optimizeDeps: {
    include: ['sql.js'],
  },
  server: {
    host: true,
    port: 3000,
    // Poll for file changes when running in Docker (bind-mounted source).
    watch: {
      usePolling: process.env.CHOKIDAR_USEPOLLING === '1',
    },
    // Keep the browser same-origin: proxy /api to the backend (the api service
    // in Docker, or a local uvicorn on the host).
    proxy: {
      '/api': {
        target: process.env.VITE_API_TARGET || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
