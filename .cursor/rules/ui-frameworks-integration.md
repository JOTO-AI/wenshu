---
description: 'UI框架集成规范：shadcn-ui、Tailwind CSS v4、Assistant UI 完整配置指南'
globs: ['**/*.tsx', '**/*.ts', '**/tailwind.config.js', '**/postcss.config.js', '**/vite.config.ts', '**/styles.css', '**/globals.css']
alwaysApply: true
---

# UI框架集成规范

## 🚨 核心原则：三框架协调配置

**本规范基于实际生产环境踩坑经验，解决 shadcn-ui + Tailwind CSS v4 + Assistant UI 集成问题！**

## 📋 框架概览

### 🎨 三大UI框架
- **shadcn-ui**: 基础组件库（Button、Card、Input等）
- **Tailwind CSS v4**: 样式框架（新版本配置方式）
- **Assistant UI**: 聊天界面组件（Thread、Message等）

### 🔗 集成挑战
1. **样式文件导入顺序**：影响CSS优先级和变量定义
2. **Tailwind v4 配置**：新版本配置方式与v3不同
3. **自定义颜色生成**：CSS变量到Tailwind类的映射
4. **框架间兼容性**：避免样式冲突和重复定义

## 🛠️ 核心配置文件

### 1. 样式文件导入（关键！）

**apps/web-app/src/main.tsx**
```typescript
import { StrictMode } from 'react';
import * as ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './app/app';
import './styles.css'; // ✅ 必须导入！

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
```

**apps/web-app/src/styles.css**
```css
/* Import UI library styles (includes Tailwind directives) */
@import '@wenshu/ui/styles';

/* You can add global styles to this file, and also import other style files */
```

### 2. Tailwind CSS v4 配置

**apps/web-app/tailwind.config.js**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class'], // ✅ 支持暗色模式
  content: [
    join(__dirname, '{src,pages,components,app}/**/*!(*.stories|*.spec).{ts,tsx,html}'),
    join(__dirname, '../../libs/ui/src/**/*.{ts,tsx}'), // ✅ 包含UI库
    ...createGlobPatternsForDependencies(__dirname),
  ],
  theme: {
    colors: { // ✅ 注意：直接在 theme.colors 而不是 theme.extend.colors
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
      // ... 其他颜色定义
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

**apps/web-app/postcss.config.js**
```javascript
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

### 3. UI库样式配置

**libs/ui/src/styles/globals.css**
```css
@import 'tw-animate-css';
@import 'tailwindcss';

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --secondary: 0 0% 96.1%;
    --muted: 0 0% 96.1%;
    --accent: 0 0% 96.1%;
    --border: 0 0% 89.8%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --secondary: 0 0% 14.9%;
    --muted: 0 0% 14.9%;
    --accent: 0 0% 14.9%;
    --border: 0 0% 14.9%;
  }
}

@layer base {
  * {
    border-color: hsl(var(--border));
    outline-color: hsl(var(--ring) / 0.5);
  }
  body {
    background-color: hsl(var(--background));
    color: hsl(var(--foreground));
  }
}

/* ✅ Tailwind v4 兼容性修复：手动定义自定义颜色类 */
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
  .bg-accent {
    background-color: hsl(var(--accent));
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
  .text-foreground {
    color: hsl(var(--foreground));
  }
  .border-border {
    border-color: hsl(var(--border));
  }
}
```

## 🔧 框架特定配置

### shadcn-ui 配置

**libs/ui/components.json**
```json
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
  "aliases": {
    "components": "./src/components",
    "utils": "./src/lib/utils",
    "ui": "./src/components/ui"
  }
}
```

### Assistant UI 集成

**正确的使用方式**：
```typescript
import {
  AssistantRuntimeProvider,
  ThreadPrimitive,
  useLocalRuntime,
} from '@assistant-ui/react';

function ChatPage() {
  const runtime = useLocalRuntime({
    async run({ messages }) {
      // API 调用逻辑
      return { content: [{ type: 'text', text: 'Response' }] };
    },
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <ThreadPrimitive.Root className="h-full">
        <ThreadPrimitive.Viewport className="h-full p-4">
          <ThreadPrimitive.Messages />
        </ThreadPrimitive.Viewport>
      </ThreadPrimitive.Root>
    </AssistantRuntimeProvider>
  );
}
```

## 🚨 常见问题和解决方案

### 问题1: 自定义颜色不显示

**症状**: `bg-primary`, `bg-secondary` 等显示为透明
**原因**: Tailwind CSS v4 不自动生成自定义颜色类
**解决**: 在 `globals.css` 中手动添加 `@layer utilities` 部分

### 问题2: 样式文件未加载

**症状**: 页面完全无样式或使用默认浏览器样式
**原因**: `main.tsx` 中未导入样式文件
**解决**: 添加 `import './styles.css'`

### 问题3: PostCSS 解析错误

**症状**: `Missing "./base" specifier in "tailwindcss" package`
**原因**: 尝试使用 Tailwind v3 的导入方式
**解决**: 使用 `@import 'tailwindcss'` 而不是 `@import 'tailwindcss/base'`

### 问题4: 组件样式冲突

**症状**: shadcn-ui 和 Assistant UI 组件样式互相覆盖
**原因**: CSS 优先级和导入顺序问题
**解决**: 确保正确的导入顺序和使用 CSS layers

## ✅ 开发流程检查清单

### 新项目初始化
- [ ] 确认 `main.tsx` 中导入了样式文件
- [ ] 验证 `tailwind.config.js` 配置正确
- [ ] 检查 `postcss.config.js` 配置
- [ ] 确认 UI 库的 `globals.css` 包含自定义颜色类

### 添加新组件时
- [ ] 使用正确的导入路径（相对路径 vs 工作区别名）
- [ ] 验证组件样式正确显示
- [ ] 检查是否与现有组件样式冲突
- [ ] 运行类型检查和构建验证

### 样式修改后
- [ ] 清理缓存：`rm -rf node_modules/.vite`
- [ ] 重启开发服务器
- [ ] 验证所有颜色类正常工作
- [ ] 检查暗色模式兼容性

### 部署前检查
- [ ] 运行完整构建：`pnpm exec nx build @wenshu/web-app`
- [ ] 验证生产环境样式正确
- [ ] 检查 CSS 文件大小和优化
- [ ] 确认所有框架功能正常

## 🔍 故障排除命令

```bash
# 清理所有缓存
rm -rf node_modules/.vite && rm -rf apps/web-app/node_modules/.vite

# 重新安装依赖
pnpm install --frozen-lockfile

# 验证构建
pnpm exec nx build @wenshu/web-app

# 检查类型
pnpm exec nx typecheck @wenshu/web-app

# 检查样式文件
find . -name "*.css" -exec grep -l "tailwindcss" {} \;
```

---

**记住：UI框架集成的关键是正确的配置顺序和兼容性处理。遇到问题时，先检查配置文件，再检查导入顺序！**
