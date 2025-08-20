/// <reference types='vitest' />
import { nxViteTsPaths } from '@nx/vite/plugins/nx-tsconfig-paths.plugin';

import react from '@vitejs/plugin-react';
import path from 'path';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(async ({ mode }) => {
  // 从工作区根目录加载环境变量
  const env = loadEnv(mode, path.resolve(__dirname, '../../'), '');
  const port = parseInt(env.WEB_APP_PORT || '3000');

  // Tailwind CSS v3 不需要动态导入

  return {
    root: __dirname,
    cacheDir: '../../node_modules/.vite/apps/web-app',
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
    plugins: [react(), nxViteTsPaths()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@workspace/ui': path.resolve(__dirname, '../../packages/ui/src'),
      },
    },
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
