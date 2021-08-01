import { defineConfig } from 'vite'
import reactRefresh from '@vitejs/plugin-react-refresh'

// https://vitejs.dev/config/
export default defineConfig({
  build: { manifest: true }, // On build, generate manifest.json (Django will use it to determine what frontend files to serve)
  base: process.env === ('production' as unknown as NodeJS.ProcessEnv) ? 'static' : '/', // Needed because Django expects all assets to be within a static folder in production; not used in development
  root: './src', // Root folder where all frontend files are located
  plugins: [reactRefresh()], // Fast-refresh (and hot-module reloading) hotness
})
