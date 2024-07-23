import { defineConfig } from 'vite';
import { djangoVitePlugin } from 'django-vite-plugin';

export default defineConfig({
  plugins: [
    djangoVitePlugin([
      'assets/js/main.js',
      'assets/js/index.js',
      'assets/css/main.css',
    ])
  ],
});
