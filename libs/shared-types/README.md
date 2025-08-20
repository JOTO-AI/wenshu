# @wenshu/shared-types

前后端共享的 TypeScript 类型定义库，确保数据结构一致性。

## 概述

这个库包含了智能问数系统中前后端共享的所有 TypeScript 类型定义，包括：

- API 请求和响应类型
- 数据模型类型
- 配置类型
- 枚举和常量

## 使用方法

### 在前端项目中使用

```typescript
import { ApiResponse, UserProfile, ChatMessage } from '@wenshu/shared-types';

// 使用共享类型
const handleApiResponse = (response: ApiResponse<UserProfile>) => {
  // 类型安全的处理逻辑
};
```

### 在后端项目中使用

```python
# Python 后端通过 TypeScript 类型生成对应的 Pydantic 模型
from shared_types import ApiResponse, UserProfile, ChatMessage
```

## 开发指南

### 添加新类型

1. 在 `src/` 目录下创建或修改类型文件
2. 确保类型定义清晰且有注释
3. 在 `src/index.ts` 中导出新类型
4. 运行类型检查确保无错误

### 构建

```bash
nx build shared-types
```

### 测试

```bash
nx test shared-types
```

## 最佳实践

- 使用描述性的类型名称
- 为复杂类型添加 JSDoc 注释
- 避免使用 `any` 类型
- 保持类型定义的向后兼容性
