/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        host: true, // Needed for Docker port mapping
        strictPort: true,
        port: 3000,
        watch: {
            usePolling: true // Needed for hot reload in some Docker environments (Windows/WSL)
        }
    },
    // Vitest Configuration
    test: {
        globals: true,
        environment: 'jsdom',
        setupFiles: './src/test/setup.ts',
        css: false,
    },
})