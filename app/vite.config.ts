import { fileURLToPath } from 'node:url'
import { defineConfig, type Plugin, type ViteDevServer } from 'vite'
import react from '@vitejs/plugin-react'

// The file whose (re)appearance means "a new build landed" — see below.
const CATALOG = fileURLToPath(new URL('public/data/catalog.json', import.meta.url))

// Reload the open tab when build_content.py regenerates public/data, so
// authoring a question doesn't need a manual reload.
//
// Vite already watches publicDir — but only to keep its public-file lookup set
// in sync. The HMR path reacts to files in the module graph, and a public/
// asset is in nobody's module graph, so a rebuild reached the watcher and then
// stopped there. The missing piece is purely the notification, hence a plugin
// rather than more watch configuration.
//
// Watching catalog.json alone, and only for add/change, is what makes this
// exact rather than merely debounced. build_content.py writes a sibling .tmp
// directory, deletes public/data and renames the new tree into place, so one
// rebuild is ~270 watcher events: through a bind mount with polling they arrive
// over more than a second, and any debounce short enough to feel instant fired
// twice. catalog.json is written INSIDE the temp tree, so it reaches its final
// path only in the rename — its 'add' fires exactly once per rebuild, and only
// once every other file is already in place. Reacting to the deletions instead
// would reload the tab during the ~1s window when public/data does not exist.
function reloadOnContentRebuild(): Plugin {
  return {
    name: 'reload-on-content-rebuild',
    apply: 'serve',
    configureServer(server: ViteDevServer) {
      let timer: ReturnType<typeof setTimeout> | null = null
      const rebuilt = (file: string) => {
        if (file !== CATALOG) return
        // Short debounce: polling can report the rename as add-then-change.
        if (timer) clearTimeout(timer)
        timer = setTimeout(() => {
          timer = null
          server.config.logger.info('content rebuilt, reloading', { timestamp: true })
          server.ws.send({ type: 'full-reload' })
        }, 300)
      }
      server.watcher.on('add', rebuilt)
      server.watcher.on('change', rebuilt)
    },
  }
}

export default defineConfig({
  plugins: [react(), reloadOnContentRebuild()],
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
