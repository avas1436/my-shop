// vite.config.js

// ساده سازی مسیر پوشه ها با شروع از @
import { fileURLToPath, URL } from 'node:url'

// پلاگین وایت
import vue from '@vitejs/plugin-vue'

// TypeScript / IntelliSense
import { defineConfig } from 'vite'

// Progressive Web App
import { VitePWA } from 'vite-plugin-pwa'

// برای فعال کردن سریع تر و بهتر نسخه توسعه و پروداکشن
import vueDevTools from 'vite-plugin-vue-devtools'

// نمایش حجم نهایی اپ
// stats.html
import { visualizer } from 'rollup-plugin-visualizer'

// است ساختار کلی تنظیمات است
// export default defineConfig({
//   plugins: [ ],
//   resolve: { }
// })

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    visualizer({
      gzipSize: true,
      brotliSize: true,
    }),
    VitePWA({
      registerType: 'autoUpdate', // آپدیت بدون مزاحمت برای کاربر
      injectRegister: 'auto',
      includeAssets: ['favicon.ico'],
      manifest: {
        name: 'Shop Frontend',
        short_name: 'Shop',
        theme_color: '#0f766e',
        background_color: '#f8fafc',
        display: 'standalone',
        icons: [
          { src: '/pwa-192x192.png', sizes: '192x192', type: 'image/png' },
          { src: '/pwa-512x512.png', sizes: '512x512', type: 'image/png' },
          {
            src: '/pwa-512x512-maskable.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
        ],
      },
      workbox: {
        // App Shell برای SPA
        navigateFallback: '/index.html',
        navigateFallbackDenylist: [
          /^\/v1\//, // API
          /^\/assets\//, // فایل‌های استاتیک
          /^\/sw\.js$/, // سرویس‌ورکر
        ],
        runtimeCaching: [
          {
            urlPattern: ({ request }) => request.destination === 'image',
            handler: 'CacheFirst',
            options: {
              cacheName: 'image-cache',
              expiration: {
                maxEntries: 120,
                maxAgeSeconds: 60 * 60 * 24 * 14,
              },
            },
          },
          {
            urlPattern: ({ url, request }) =>
              request.method === 'GET' && url.pathname.startsWith('/v1/'),
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-get-cache',
              networkTimeoutSeconds: 5,
              expiration: {
                maxEntries: 80,
                maxAgeSeconds: 60 * 60 * 24,
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: ({ request }) =>
              request.destination === 'style' || request.destination === 'font',
            handler: 'StaleWhileRevalidate',
            options: { cacheName: 'assets-cache' },
          },
        ],
        // navigateFallback: '/offline.html', نمایش یک صفحه برای مواقع آفلاین بودن
      },
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
