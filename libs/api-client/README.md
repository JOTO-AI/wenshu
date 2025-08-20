# @wenshu/api-client

统一的 API 客户端库，封装所有后端 API 调用逻辑。

## 概述

这个库提供了与智能问数系统后端 API 交互的统一接口，包括：

- HTTP 客户端配置
- API 端点封装
- 错误处理
- 类型安全的请求和响应
- 认证和授权处理

## 使用方法

### 基本用法

```typescript
import { apiClient } from '@wenshu/api-client';

// 获取用户信息
const userProfile = await apiClient.users.getProfile();

// 发送聊天消息
const response = await apiClient.chat.sendMessage({
  message: '分析销售数据',
  sessionId: 'session-123',
});
```

### 配置客户端

```typescript
import { createApiClient } from '@wenshu/api-client';

const client = createApiClient({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

### 错误处理

```typescript
import { ApiError } from '@wenshu/api-client';

try {
  const data = await apiClient.data.query(params);
} catch (error) {
  if (error instanceof ApiError) {
    console.error('API Error:', error.message, error.status);
  }
}
```

## API 模块

### 用户管理 (users)

- `getProfile()` - 获取用户资料
- `updateProfile(data)` - 更新用户资料
- `getPermissions()` - 获取用户权限

### 聊天对话 (chat)

- `sendMessage(params)` - 发送消息
- `getHistory(sessionId)` - 获取对话历史
- `createSession()` - 创建新会话

### 数据查询 (data)

- `query(params)` - 执行数据查询
- `getDataSources()` - 获取数据源列表
- `validateQuery(query)` - 验证查询语句

## 开发指南

### 添加新的 API 端点

1. 在相应的模块文件中添加方法
2. 使用 `@wenshu/shared-types` 中的类型
3. 添加适当的错误处理
4. 编写单元测试

### 构建

```bash
nx build api-client
```

### 测试

```bash
nx test api-client
```

## 配置选项

| 选项    | 类型   | 默认值                  | 描述              |
| ------- | ------ | ----------------------- | ----------------- |
| baseURL | string | 'http://localhost:8000' | API 基础 URL      |
| timeout | number | 5000                    | 请求超时时间 (ms) |
| retries | number | 3                       | 重试次数          |
| headers | object | {}                      | 默认请求头        |
