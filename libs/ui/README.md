# @wenshu/ui

智能问数平台的统一 UI 组件库。

## 架构设计

这个库遵循 DRY、KISS、YAGNI 原则，提供了三类主要的 UI 组件：

### 📦 组件分类

#### 🎨 基础组件 (`ui/`)

基于 shadcn-ui 的通用基础组件，所有应用都可以使用：

- `Button` - 按钮组件
- `Card` - 卡片组件系列
- `Input` - 输入框组件

#### 📊 图表组件 (`charts/`)

基于 Recharts 的数据可视化组件，主要用于 Admin 后台：

- `ChartContainer` - 响应式图表容器
- `LineChart` - 折线图
- `BarChart` - 柱状图

#### 💬 聊天组件 (`chat/`)

用于构建聊天界面的组件，主要用于 Client 应用：

- `ChatInterface` - 完整的聊天界面
- `Message` - 单条消息组件
- `Composer` - 消息输入组件

### 🛠️ 工具函数 (`lib/`)

- `cn()` - Tailwind 样式合并工具
- 其他通用工具函数

### 🎨 样式 (`styles/`)

- `globals.css` - 全局样式和主题变量

## 使用方式

### 安装依赖

```bash
# 在需要使用的应用中添加依赖
pnpm add @wenshu/ui
```

### 导入样式

在应用的根组件中导入样式：

```tsx
import '@wenshu/ui/styles';
```

### 使用组件

#### 基础组件（所有应用通用）

```tsx
import { Button, Card, Input } from '@wenshu/ui';

function MyComponent() {
  return (
    <Card>
      <Input placeholder='输入内容' />
      <Button>提交</Button>
    </Card>
  );
}
```

#### 图表组件（Admin 应用）

```tsx
import { LineChart, BarChart, ChartContainer } from '@wenshu/ui';

const data = [
  { name: '一月', value: 100 },
  { name: '二月', value: 200 },
];

function AdminDashboard() {
  return (
    <LineChart
      data={data}
      xDataKey='name'
      lines={[{ dataKey: 'value', stroke: '#3b82f6' }]}
    />
  );
}
```

#### 聊天组件（Client 应用）

```tsx
import { ChatInterface } from '@wenshu/ui';

function ClientChat() {
  return (
    <ChatInterface
      title='智能助手'
      placeholder='问我任何问题...'
      onSendMessage={message => console.log('发送消息:', message)}
    />
  );
}
```

## 开发指南

### 构建

```bash
pnpm exec nx build ui
```

### 类型检查

```bash
pnpm exec nx typecheck ui
```

### 测试

```bash
pnpm exec nx test ui
```

## 设计原则

1. **DRY (Don't Repeat Yourself)** - 避免重复，统一管理所有 UI 组件
2. **KISS (Keep It Simple, Stupid)** - 保持简单，只实现必要的功能
3. **YAGNI (You Aren't Gonna Need It)** - 不做过度设计，按需实现功能
4. **组件分离** - 按使用场景分类组织，便于按需导入
5. **类型安全** - 提供完整的 TypeScript 支持
