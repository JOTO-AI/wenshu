# @workspace/ui

基于 shadcn-ui 的 UI 组件库，为智能问数系统提供统一的设计系统和组件。

## 概述

这个库集成了 shadcn-ui 组件系统，使用 Tailwind CSS v3.4.15 进行样式管理，提供：

- 完整的 shadcn-ui 组件集合
- 统一的设计系统和主题
- TypeScript 类型支持
- 暗色主题支持
- 响应式设计
- 无障碍访问支持

## 技术栈

- **React 18.3.1** - UI 框架
- **Tailwind CSS v3.4.15** - 样式框架
- **Radix UI** - 无障碍原语组件
- **lucide-react** - 图标库
- **class-variance-authority** - 样式变体管理
- **tailwind-merge** - 样式合并工具

## 使用方法

### 在应用中导入组件

```typescript
// 从工作区导入
import { Button, Card, Dialog } from '@workspace/ui';

// 或从应用级重导出导入
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
```

### 基本组件使用

```typescript
import { Button, Card, CardContent, CardHeader, CardTitle } from '@workspace/ui';

function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>示例卡片</CardTitle>
      </CardHeader>
      <CardContent>
        <Button variant="default" size="md">
          点击按钮
        </Button>
      </CardContent>
    </Card>
  );
}
```

## 可用组件

### 基础组件
- `Button` - 按钮组件，支持多种变体和大小
- `Input` - 输入框组件
- `Card` - 卡片容器组件
- `Badge` - 徽章组件
- `Avatar` - 头像组件

### 布局组件
- `Separator` - 分隔符
- `Skeleton` - 骨架屏
- `Collapsible` - 折叠面板

### 导航组件
- `Breadcrumb` - 面包屑导航
- `Sidebar` - 侧边栏组件系统

### 反馈组件
- `Dialog` - 对话框
- `Tooltip` - 工具提示
- `DropdownMenu` - 下拉菜单

## 样式系统

### CSS 变量

组件使用 CSS 变量进行主题管理：

```css
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --primary: 240 9% 9%;
  --primary-foreground: 0 0% 98%;
  /* ... 更多变量 */
}
```

### 暗色主题

```css
.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  /* ... 暗色主题变量 */
}
```

## 开发指南

### 添加新组件

1. 使用 shadcn-ui CLI 添加组件：
```bash
cd apps/web-app
npx shadcn@latest add [component-name]
```

2. 组件会自动安装到 `packages/ui/src/components/`

3. 在 `packages/ui/src/index.ts` 中导出新组件：
```typescript
export { NewComponent } from './components/new-component';
```

### 自定义组件

```typescript
import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../lib/utils';

const customVariants = cva(
  'base-styles',
  {
    variants: {
      variant: {
        default: 'default-styles',
        secondary: 'secondary-styles',
      },
      size: {
        sm: 'small-styles',
        md: 'medium-styles',
        lg: 'large-styles',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

export interface CustomComponentProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof customVariants> {}

const CustomComponent = React.forwardRef<HTMLDivElement, CustomComponentProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(customVariants({ variant, size }), className)}
        {...props}
      />
    );
  }
);

CustomComponent.displayName = 'CustomComponent';

export { CustomComponent, customVariants };
```

## 构建和测试

### 构建

```bash
nx build @workspace/ui
```

### 类型检查

```bash
nx typecheck @workspace/ui
```

## 最佳实践

1. **使用相对路径导入**：在组件库内部使用相对路径
2. **保持组件纯净**：避免业务逻辑，专注于 UI 展示
3. **遵循 shadcn-ui 约定**：保持与官方组件的一致性
4. **提供完整的 TypeScript 类型**：确保类型安全
5. **支持主题切换**：使用 CSS 变量而不是硬编码颜色

## 故障排除

### 常见问题

1. **样式不生效**：确保 Tailwind CSS 配置包含了组件库路径
2. **类型错误**：检查 TypeScript 配置和路径映射
3. **组件不渲染**：验证所有依赖是否正确安装

### 调试技巧

```bash
# 检查构建输出
ls -la packages/ui/dist/

# 验证类型声明
cat packages/ui/dist/index.d.ts

# 检查样式编译
cat packages/ui/dist/index.css
```
