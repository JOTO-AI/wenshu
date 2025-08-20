---
description: 'Nx Monorepo UI框架集成规范：shadcn-ui、Tailwind CSS v3、Assistant UI 配置'
globs:
  [
    '**/*.tsx',
    '**/*.ts',
    '**/tailwind.config.js',
    '**/postcss.config.js',
    '**/vite.config.ts',
    '**/styles.css',
    '**/globals.css',
    '**/components.json',
  ]
alwaysApply: true
---

# Nx Monorepo UI 框架集成规范 (Tailwind CSS v3)

## 项目架构

### 目录结构

```bash
workspace/
├── apps/web-app/
│   ├── src/main.tsx              # 样式导入入口
│   ├── src/components/ui/        # UI 组件重导出
│   ├── styles.css                # 应用级样式
│   ├── tailwind.config.js        # Tailwind v3 配置
│   ├── postcss.config.js         # PostCSS 配置
│   └── components.json           # shadcn-ui 配置
└── packages/ui/                  # shadcn-ui 组件库
    ├── src/
    │   ├── components/            # shadcn-ui组件
    │   ├── styles/globals.css     # 全局样式和CSS变量 (v3语法)
    │   ├── lib/utils.ts           # cn函数和工具
    │   └── index.ts               # 统一导出
    ├── components.json            # shadcn-ui配置
    └── package.json
```

### 包依赖设置

```json
// apps/web-app/package.json
{
  "dependencies": {
    "@workspace/ui": "workspace:*"
  }
}
```

## 核心配置

### 样式文件导入

#### 主入口

```typescript
// apps/web-app/src/main.tsx
import { StrictMode } from 'react';
import * as ReactDOM from 'react-dom/client';
import App from './app/app';
import './styles.css'; // 必须导入！包含UI库样式
```

#### 样式导入

```css
/* apps/web-app/src/styles.css */
@import '@workspace/ui/styles/globals.css';
```

### Tailwind 配置

#### Tailwind 设置

```javascript
// apps/web-app/tailwind.config.js
const { createGlobPatternsForDependencies } = require('@nx/react/tailwind');
const { join } = require('path');

module.exports = {
  darkMode: ['class'],
  content: [
    join(
      __dirname,
      '{src,pages,components,app}/**/*!(*.stories|*.spec).{ts,tsx,html}'
    ),
    join(__dirname, '../../libs/ui/src/**/*.{ts,tsx}'), // 包含UI库组件
    ...createGlobPatternsForDependencies(__dirname), // Nx优化
  ],
  theme: {
    colors: {
      // 直接在 theme.colors 而不是 theme.extend.colors
      border: 'hsl(var(--border))',
      input: 'hsl(var(--input))',
      ring: 'hsl(var(--ring))',
      background: 'hsl(var(--background))',
      foreground: 'hsl(var(--foreground))',
      primary: {
        DEFAULT: 'hsl(var(--primary))',
        foreground: 'hsl(var(--primary-foreground))',
      },
      secondary: {
        DEFAULT: 'hsl(var(--secondary))',
        foreground: 'hsl(var(--secondary-foreground))',
      },
      muted: {
        DEFAULT: 'hsl(var(--muted))',
        foreground: 'hsl(var(--muted-foreground))',
      },
      accent: {
        DEFAULT: 'hsl(var(--accent))',
        foreground: 'hsl(var(--accent-foreground))',
      },
      card: {
        DEFAULT: 'hsl(var(--card))',
        foreground: 'hsl(var(--card-foreground))',
      },
    },
    extend: {
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
  plugins: [],
};
```

#### PostCSS 设置

```javascript
// apps/web-app/postcss.config.js
const { join } = require('path');

module.exports = {
  plugins: {
    '@tailwindcss/postcss': {
      config: join(__dirname, 'tailwind.config.js'),
    },
    autoprefixer: {},
  },
};
```

### UI 库样式

```css
/* libs/ui/src/styles/globals.css */
@import 'tw-animate-css';
@import 'tailwindcss';

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    --secondary: 0 0% 96.1%;
    --secondary-foreground: 0 0% 9%;
    --muted: 0 0% 96.1%;
    --muted-foreground: 0 0% 45.1%;
    --accent: 0 0% 96.1%;
    --accent-foreground: 0 0% 9%;
    --border: 0 0% 89.8%;
    --input: 0 0% 89.8%;
    --ring: 0 0% 3.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 0 0% 9%;
    --secondary: 0 0% 14.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 0 0% 14.9%;
    --muted-foreground: 0 0% 63.9%;
    --accent: 0 0% 14.9%;
    --accent-foreground: 0 0% 98%;
    --border: 0 0% 14.9%;
    --input: 0 0% 14.9%;
    --ring: 0 0% 83.1%;
  }

  * {
    border-color: hsl(var(--border));
    outline-color: hsl(var(--ring) / 0.5);
  }
  body {
    background-color: hsl(var(--background));
    color: hsl(var(--foreground));
  }
}

/* Tailwind v4 兼容性修复：手动定义自定义颜色类 */
@layer utilities {
  .bg-primary {
    background-color: hsl(var(--primary));
  }
  .bg-secondary {
    background-color: hsl(var(--secondary));
  }
  .bg-muted {
    background-color: hsl(var(--muted));
  }
  .text-primary {
    color: hsl(var(--primary));
  }
  .text-secondary {
    color: hsl(var(--secondary));
  }
  .text-muted-foreground {
    color: hsl(var(--muted-foreground));
  }
  .border-border {
    border-color: hsl(var(--border));
  }
}
```

## shadcn-ui 配置

### 配置文件

```json
// libs/ui/components.json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/styles/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "iconLibrary": "lucide",
  "aliases": {
    "components": "./src/components",
    "utils": "./src/lib/utils",
    "ui": "./src/components/ui"
  }
}
```

### 开发工作流

```bash
# 在 UI 库中添加组件
cd libs/ui
npx shadcn@latest add button card input

# 更新导出文件
# libs/ui/src/index.ts
export { Button } from './components/ui/button';
export { Card, CardContent, CardHeader } from './components/ui/card';

# 在应用中使用
import { Button, Card } from '@wenshu/ui';
```

## Assistant UI 集成

### 基本用法

```typescript
import {
  AssistantRuntimeProvider,
  ThreadPrimitive,
  useLocalRuntime,
} from '@assistant-ui/react';
import { Card, CardContent, ScrollArea } from '@wenshu/ui';

function ChatInterface() {
  const runtime = useLocalRuntime({
    async run({ messages }) {
      return { content: [{ type: 'text', text: 'Response' }] };
    },
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <Card className='h-[600px]'>
        <CardContent className='p-0'>
          <ThreadPrimitive.Root>
            <ScrollArea className='h-[500px]'>
              <ThreadPrimitive.Viewport className='p-4'>
                <ThreadPrimitive.Messages />
              </ThreadPrimitive.Viewport>
            </ScrollArea>
          </ThreadPrimitive.Root>
        </CardContent>
      </Card>
    </AssistantRuntimeProvider>
  );
}
```

## 常见问题解决

### 颜色问题

在 `libs/ui/src/styles/globals.css` 中添加 `@layer utilities` 自定义颜色类

### 样式加载

确保在 `apps/web-app/src/main.tsx` 中添加 `import './styles.css'`

### 依赖问题

```bash
# 重建 UI 库
pnpm exec nx build ui
# 重新安装依赖
pnpm install --frozen-lockfile
```

### 缓存问题

```bash
pnpm exec nx reset
```

## 检查清单

### 项目初始化

- 确认 `main.tsx` 导入样式文件
- 验证 `tailwind.config.js` 配置
- 检查 UI 库 `globals.css` 包含自定义颜色类
- 验证 workspace 依赖配置

### 组件开发

- 在 `libs/ui` 中使用 `npx shadcn@latest add <component>`
- 更新 `libs/ui/src/index.ts` 导出
- 运行类型检查：`pnpm exec nx typecheck ui`
- 在应用中测试组件功能

### 故障排除

```bash
# 清理缓存
pnpm exec nx reset
rm -rf node_modules/.cache

# 重新构建
pnpm exec nx build ui --skip-nx-cache
pnpm exec nx build @wenshu/web-app --prod

# 类型检查
pnpm exec nx typecheck ui
pnpm exec nx typecheck @wenshu/web-app
```
