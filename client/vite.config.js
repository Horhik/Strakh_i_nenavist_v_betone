import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 5173, // Dev server for Svelte
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Flask server
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
