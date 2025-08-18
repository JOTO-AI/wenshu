---
description: '前端架构重构指南：基于DRY、KISS、YAGNI原则的务实重构'
globs: ['**/*.tsx', '**/*.ts', '**/routes/*.tsx']
alwaysApply: true
---

# 前端架构重构指南

## 🎯 核心设计原则

### DRY (Don't Repeat Yourself)
- **避免重复代码**：提取共同逻辑，但不要过度抽象
- **统一目录结构**：避免多套目录架构并存
- **一致的导入模式**：统一使用相对路径或工作区别名

### KISS (Keep It Simple, Stupid)
- **保持简单**：避免过度设计和不必要的复杂性
- **清晰的职责分离**：每个目录和文件有明确的作用
- **直观的命名**：目录和文件名能够自我解释

### YAGNI (You Aren't Gonna Need It)
- **不实现当前不需要的功能**：避免为了"未来可能"而过度设计
- **务实的重构**：只解决实际存在的问题
- **渐进式改进**：小步快跑，逐步优化

## 📋 重构案例：pages/ 目录整合

### 问题识别

**发现的架构不一致**：
- 存在独立的 `apps/web-app/src/pages/` 目录
- 项目主要使用 `features/` 架构
- 造成两套目录结构并存，违反DRY原则

**文件分析**：
```typescript
// 原位置：apps/web-app/src/pages/test-ui.tsx
// 作用：UI组件测试页面，用于验证UI框架集成
// 路由：/test-ui
// 价值：开发和调试工具，有实际使用价值
```

### 重构方案

**目标**：统一目录架构，保持功能完整性

**新位置**：`apps/web-app/src/features/client/dev/pages/test-ui.tsx`

**理由**：
- ✅ 符合 features 架构模式
- ✅ 明确标识为开发工具
- ✅ 保持在客户端路由中的可访问性
- ✅ 避免创建独立的目录结构

### 重构步骤

1. **创建新目录结构**
   ```bash
   mkdir -p apps/web-app/src/features/client/dev/pages
   ```

2. **移动文件**
   ```bash
   mv apps/web-app/src/pages/test-ui.tsx apps/web-app/src/features/client/dev/pages/test-ui.tsx
   ```

3. **更新路由引用**
   ```typescript
   // apps/web-app/src/routes/client-routes.tsx
   // 修改前
   const TestUIPage = lazy(() => import('../pages/test-ui'));
   
   // 修改后
   const TestUIPage = lazy(() => import('../features/client/dev/pages/test-ui'));
   ```

4. **验证功能完整性**
   ```bash
   pnpm exec nx typecheck @wenshu/web-app
   pnpm exec nx build @wenshu/web-app
   ```

5. **清理旧结构**
   ```bash
   rmdir apps/web-app/src/pages
   ```

### 重构结果

**架构改进**：
- ✅ 统一了目录结构，消除了重复
- ✅ 保持了功能完整性
- ✅ 提高了代码组织的一致性
- ✅ 明确了开发工具的归属

**验证指标**：
- ✅ 类型检查通过
- ✅ 构建成功
- ✅ 路由功能正常
- ✅ 测试页面可访问

## 🏗️ 当前架构规范

### 统一的目录结构

```
apps/web-app/src/
├── features/               # 按角色和功能分组的模块
│   ├── client/            # 普通用户功能
│   │   ├── chat/          # 聊天功能
│   │   ├── dashboard/     # 仪表板
│   │   ├── profile/       # 个人设置
│   │   └── dev/           # 开发工具（UI测试等）
│   └── admin/             # 管理员功能
│       ├── analytics/     # 管理统计
│       ├── permissions/   # 权限管理
│       └── ...
├── routes/                # 路由配置
├── layouts/               # 布局组件
├── components/            # 应用特定组件
├── auth/                  # 认证模块
├── shared/                # 共享组件和工具
├── middleware/            # 权限中间件
└── stores/                # 全局状态管理
```

### 架构原则

1. **功能模块化**：按业务功能和用户角色组织代码
2. **职责分离**：每个目录有明确的职责边界
3. **一致性**：统一的命名和组织模式
4. **可扩展性**：便于添加新功能模块
5. **可维护性**：清晰的依赖关系和导入路径

### 开发工具归属

**原则**：开发工具和测试页面统一放在对应角色的 `dev/` 目录下

**示例**：
- 客户端开发工具：`features/client/dev/`
- 管理端开发工具：`features/admin/dev/`
- 通用开发工具：`shared/dev/`

## 🔧 重构最佳实践

### 重构前检查清单

- [ ] 识别实际存在的架构问题
- [ ] 评估重构的必要性和价值
- [ ] 确保不破坏现有功能
- [ ] 制定明确的验证标准

### 重构执行原则

- [ ] 小步快跑，逐步改进
- [ ] 每次重构后立即验证
- [ ] 保持功能完整性
- [ ] 更新相关文档

### 重构后验证

- [ ] 运行类型检查：`pnpm exec nx typecheck @wenshu/web-app`
- [ ] 验证构建成功：`pnpm exec nx build @wenshu/web-app`
- [ ] 测试关键功能路径
- [ ] 更新架构文档

## 📚 相关规范文档

- **TypeScript 前端开发规范**：`.cursor/rules/typescript-frontend.mdc`
- **UI框架集成规范**：`.cursor/rules/ui-frameworks-integration.md`
- **错误调试检查清单**：`.cursor/rules/error-debugging-checklist.mdc`

---

**记住：好的架构是演进出来的，不是设计出来的。基于实际问题进行务实的重构，比追求理论上的完美更有价值。**
