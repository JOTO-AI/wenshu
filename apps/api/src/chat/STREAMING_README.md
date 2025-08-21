# Dify 流式响应优化文档

## 概述

本文档说明了对 `DifyService` 类的流式响应优化，解决了之前遇到的 `text/event-stream` 解析错误问题。

## 问题背景

之前的实现在处理 Dify 流式响应时会遇到以下错误：
```
Network error calling Dify API: 200, message='Attempt to decode JSON with unexpected mimetype: text/event-stream; charset=utf-8'
```

这是因为 Dify 的流式响应使用 Server-Sent Events (SSE) 格式，内容类型为 `text/event-stream`，而不是标准的 JSON 响应。

## 优化方案

### 1. 新增流式请求方法

添加了 `_make_streaming_request()` 方法，专门处理 SSE 格式的流式响应：

```python
async def _make_streaming_request(
    self,
    method: str,
    endpoint: str,
    data: Dict[str, Any] = None,
    params: Dict[str, Any] = None
) -> AsyncGenerator[Dict[str, Any], None]:
    """发送HTTP流式请求"""
```

### 2. 增强的消息发送方法

优化了 `send_message()` 方法，支持根据 `stream` 参数自动选择合适的请求方式：

```python
async def send_message(
    self,
    query: str,
    conversation_id: Optional[str] = None,
    inputs: Optional[Dict] = None,
    stream: bool = False,  # 关键参数
    files: Optional[List[Dict]] = None,
    user: Optional[str] = None
):
```

### 3. 流式事件解析

新增 `parse_stream_event()` 方法，解析不同类型的流式事件：

- `workflow_started`: 工作流开始
- `node_started`: 节点开始
- `node_finished`: 节点完成  
- `message`: 消息内容
- `message_end`: 消息结束

### 4. 便捷方法

添加了多个便捷方法：

- `send_message_stream()`: 专用流式消息方法
- `collect_stream_response()`: 收集完整流式响应
- `parse_stream_event()`: 解析流式事件

## 使用方式

### 基本流式使用

```python
dify_service = DifyService(
    base_url="https://dify.jototech.cn/v1",
    api_key="your-api-key",
    timeout=30
)

# 方法1: 使用 send_message 流式模式
stream_generator = await dify_service.send_message(
    query="你好",
    stream=True,  # 启用流式响应
    user="user_id"
)

async for event in stream_generator:
    parsed_event = dify_service.parse_stream_event(event)
    if parsed_event["event_type"] == "message":
        print(parsed_event.get("answer", ""), end="")
```

### 事件处理示例

```python
async for event in stream_generator:
    parsed_event = dify_service.parse_stream_event(event)
    event_type = parsed_event["event_type"]
    
    if event_type == "workflow_started":
        print(f"工作流开始: {parsed_event.get('workflow_id')}")
        
    elif event_type == "node_started":
        print(f"节点开始: {parsed_event.get('title')}")
        
    elif event_type == "message":
        answer_part = parsed_event.get("answer", "")
        print(answer_part, end="", flush=True)
        
    elif event_type == "message_end":
        usage = parsed_event.get("usage", {})
        print(f"\n使用情况: {usage}")
```

### 收集完整响应

```python
stream_generator = await dify_service.send_message(
    query="解释人工智能",
    stream=True,
    user="user_id"
)

# 收集所有流式事件为完整响应
complete_response = await dify_service.collect_stream_response(stream_generator)

print(f"完整回答: {complete_response['answer']}")
print(f"消息ID: {complete_response['message_id']}")
print(f"会话ID: {complete_response['conversation_id']}")
print(f"事件总数: {complete_response['total_events']}")
```

### 非流式使用（保持兼容）

```python
# 非流式模式保持不变
response = await dify_service.send_message(
    query="你好",
    stream=False,  # 或省略，默认为 False
    user="user_id"
)

print(f"回答: {response.get('answer')}")
```

## Dify 流式事件格式

Dify 返回的 SSE 格式示例：

```
data: {"event": "workflow_started", "task_id": "xxx", "workflow_run_id": "xxx", "data": {...}}

data: {"event": "node_started", "task_id": "xxx", "workflow_run_id": "xxx", "data": {...}}

data: {"event": "node_finished", "task_id": "xxx", "workflow_run_id": "xxx", "data": {...}}

data: {"event": "message", "task_id": "xxx", "data": {"answer": "部分回答内容"}}

data: {"event": "message_end", "task_id": "xxx", "data": {"usage": {...}}}
```

## 错误处理

优化后的实现包含完整的错误处理：

- 网络错误重试
- 认证错误处理 (401)
- 速率限制处理 (429)
- JSON 解析错误容错
- 连接超时处理

## 性能优化

1. **连接复用**: 使用持久化的 HTTP 会话
2. **异步处理**: 完全异步的流式处理
3. **内存效率**: 事件逐个处理，不在内存中累积
4. **错误容错**: 单个事件解析失败不影响整体流程

## 向后兼容性

- 保持原有 API 接口不变
- 非流式调用行为完全兼容
- 现有代码无需修改即可使用

## 示例代码

完整的使用示例请参考 `dify_stream_example.py` 文件。

## 注意事项

1. 流式响应需要保持网络连接，注意超时设置
2. 大量流式事件可能影响性能，建议适当处理
3. 异常情况下记得关闭 HTTP 会话: `await dify_service.close()`
4. 生产环境中建议配置适当的重试和超时策略
