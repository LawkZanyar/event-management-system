import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue()
  ],
  server: {
    host: true,
    allowedHosts: [
      "innovative-truth-production-576f.up.railway.app"
    ]
  }
})