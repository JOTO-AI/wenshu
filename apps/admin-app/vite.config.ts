/// <reference types='vitest' />
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig(({ mode }) => {
  // 从工作区根目录加载环境变量
  const env = loadEnv(mode, path.resolve(__dirname, '../../'), '');
  const port = parseInt(env.ADMIN_APP_PORT || '4200');

  return {
    root: __dirname,
    cacheDir: '../../node_modules/.vite/apps/admin-app',
    server: {
      port,
      host: 'localhost',
      strictPort: false,
      open: false,
      hmr: {
        port: port + 1000,
      },
      fs: {
        allow: ['../../'],
      },
    },
    preview: {
      port,
      host: 'localhost',
    },
    plugins: [react()],
    optimizeDeps: {
      include: ['react', 'react-dom'],
      force: false,
    },
    esbuild: {
      target: 'es2020',
    },
    // Uncomment this if you are using workers.
    // worker: {
    //  plugins: [ nxViteTsPaths() ],
    // },
    build: {
      outDir: './dist',
      emptyOutDir: true,
      reportCompressedSize: true,
      commonjsOptions: {
        transformMixedEsModules: true,
      },
    },
    test: {
      watch: false,
      globals: true,
      environment: 'jsdom',
      include: ['{src,tests}/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
      reporters: ['default'],
      coverage: {
        reportsDirectory: './test-output/vitest/coverage',
        provider: 'v8' as const,
      },
    },
  };
});
