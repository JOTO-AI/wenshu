#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dify 流式响应集成测试
完整测试所有流式响应相关功能
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch


# 假设的测试用例，实际使用时需要适配具体的测试框架
class TestDifyStreamingIntegration:
    @pytest.fixture
    async def dify_service(self):
        """创建测试用的 DifyService 实例"""
        from ..chat_service import DifyService

        service = DifyService(
            base_url="https://test.dify.com/v1", api_key="test-api-key", timeout=30
        )
        yield service
        await service.close()

    @pytest.fixture
    def mock_streaming_response(self):
        """模拟流式响应数据"""
        events = [
            'data: {"event": "workflow_started", "task_id": "test-task-1", "workflow_run_id": "test-run-1", "data": {"id": "run-1", "workflow_id": "workflow-1", "created_at": 1679586595}}\n',
            'data: {"event": "node_started", "task_id": "test-task-1", "workflow_run_id": "test-run-1", "data": {"id": "node-1", "node_id": "start-node", "node_type": "start", "title": "开始", "index": 0, "created_at": 1679586595}}\n',
            'data: {"event": "node_finished", "task_id": "test-task-1", "workflow_run_id": "test-run-1", "data": {"id": "node-1", "node_id": "start-node", "status": "succeeded", "elapsed_time": 0.1}}\n',
            'data: {"event": "message", "task_id": "test-task-1", "data": {"id": "msg-1", "answer": "你好！", "conversation_id": "conv-1", "created_at": 1679586596}}\n',
            'data: {"event": "message", "task_id": "test-task-1", "data": {"id": "msg-1", "answer": "我是AI助手", "conversation_id": "conv-1", "created_at": 1679586597}}\n',
            'data: {"event": "message_end", "task_id": "test-task-1", "data": {"id": "msg-1", "usage": {"total_tokens": 50, "total_price": 0.001}, "metadata": {"retrieval_source": []}}}\n',
        ]
        return events

    async def test_parse_stream_event(self, dify_service):
        """测试流式事件解析"""

        # 测试工作流开始事件
        workflow_event = {
            "event": "workflow_started",
            "task_id": "test-task",
            "workflow_run_id": "test-run",
            "data": {
                "id": "run-1",
                "workflow_id": "workflow-1",
                "created_at": 1679586595,
            },
        }

        parsed = dify_service.parse_stream_event(workflow_event)
        assert parsed["event_type"] == "workflow_started"
        assert parsed["workflow_id"] == "workflow-1"
        assert parsed["task_id"] == "test-task"

        # 测试消息事件
        message_event = {
            "event": "message",
            "task_id": "test-task",
            "data": {
                "id": "msg-1",
                "answer": "测试回答",
                "conversation_id": "conv-1",
                "created_at": 1679586596,
            },
        }

        parsed = dify_service.parse_stream_event(message_event)
        assert parsed["event_type"] == "message"
        assert parsed["answer"] == "测试回答"
        assert parsed["message_id"] == "msg-1"
        assert parsed["conversation_id"] == "conv-1"

    @patch("aiohttp.ClientSession.request")
    async def test_streaming_request_success(
        self, mock_request, dify_service, mock_streaming_response
    ):
        """测试成功的流式请求"""

        # 模拟响应
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.content.iter_chunked = AsyncMock()

        # 创建异步迭代器来返回流式数据
        async def mock_chunks():
            for event_line in mock_streaming_response:
                yield event_line.encode("utf-8")

        mock_response.content.iter_chunked.return_value = mock_chunks()
        mock_request.return_value.__aenter__.return_value = mock_response

        # 执行流式请求
        stream_gen = dify_service._make_streaming_request(
            "POST",
            "/chat-messages",
            {"query": "测试", "response_mode": "streaming", "user": "test"},
        )

        events = []
        async for event in stream_gen:
            events.append(event)

        # 验证事件数量和内容
        assert len(events) == 6
        assert events[0]["event"] == "workflow_started"
        assert events[3]["event"] == "message"
        assert events[3]["data"]["answer"] == "你好！"
        assert events[5]["event"] == "message_end"

    @patch("aiohttp.ClientSession.request")
    async def test_send_message_stream_mode(
        self, mock_request, dify_service, mock_streaming_response
    ):
        """测试 send_message 流式模式"""

        # 模拟响应
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.content.iter_chunked = AsyncMock()

        async def mock_chunks():
            for event_line in mock_streaming_response:
                yield event_line.encode("utf-8")

        mock_response.content.iter_chunked.return_value = mock_chunks()
        mock_request.return_value.__aenter__.return_value = mock_response

        # 测试流式消息发送
        stream_gen = await dify_service.send_message(
            query="你好", stream=True, user="test_user"
        )

        message_parts = []
        events_count = 0

        async for event in stream_gen:
            events_count += 1
            parsed_event = dify_service.parse_stream_event(event)

            if parsed_event["event_type"] == "message":
                answer = parsed_event.get("answer", "")
                if answer:
                    message_parts.append(answer)

        full_message = "".join(message_parts)
        assert events_count == 6
        assert full_message == "你好！我是AI助手"

    @patch("aiohttp.ClientSession.request")
    async def test_collect_stream_response(
        self, mock_request, dify_service, mock_streaming_response
    ):
        """测试收集完整流式响应"""

        # 模拟响应
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.content.iter_chunked = AsyncMock()

        async def mock_chunks():
            for event_line in mock_streaming_response:
                yield event_line.encode("utf-8")

        mock_response.content.iter_chunked.return_value = mock_chunks()
        mock_request.return_value.__aenter__.return_value = mock_response

        # 获取流式响应
        stream_gen = await dify_service.send_message(
            query="测试收集", stream=True, user="test_user"
        )

        # 收集完整响应
        complete_response = await dify_service.collect_stream_response(stream_gen)

        # 验证收集的数据
        assert complete_response["answer"] == "你好！我是AI助手"
        assert complete_response["conversation_id"] == "conv-1"
        assert complete_response["message_id"] == "msg-1"
        assert complete_response["total_events"] == 6
        assert complete_response["usage"]["total_tokens"] == 50

    @patch("aiohttp.ClientSession.request")
    async def test_streaming_error_handling(self, mock_request, dify_service):
        """测试流式请求错误处理"""

        # 测试 401 错误
        mock_response = AsyncMock()
        mock_response.status = 401
        mock_request.return_value.__aenter__.return_value = mock_response

        with pytest.raises(Exception):  # 应该抛出 AuthenticationError
            stream_gen = dify_service._make_streaming_request(
                "POST", "/chat-messages", {}
            )
            async for _ in stream_gen:
                pass

        # 测试 429 错误
        mock_response.status = 429
        with pytest.raises(Exception):  # 应该抛出 RateLimitError
            stream_gen = dify_service._make_streaming_request(
                "POST", "/chat-messages", {}
            )
            async for _ in stream_gen:
                pass

    async def test_malformed_sse_handling(self, dify_service):
        """测试畸形 SSE 数据处理"""

        # 模拟畸形的 SSE 数据
        malformed_data = [
            'data: {"event": "message", "malformed": json\n',  # 无效 JSON
            "data: \n",  # 空数据
            "event: message\n",  # 非数据行
            'data: {"event": "valid", "data": {"answer": "正常"}}\n',  # 正常数据
            ": comment line\n",  # SSE 注释
        ]

        with patch("aiohttp.ClientSession.request") as mock_request:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.content.iter_chunked = AsyncMock()

            async def mock_chunks():
                for line in malformed_data:
                    yield line.encode("utf-8")

            mock_response.content.iter_chunked.return_value = mock_chunks()
            mock_request.return_value.__aenter__.return_value = mock_response

            stream_gen = dify_service._make_streaming_request(
                "POST", "/chat-messages", {}
            )

            valid_events = []
            async for event in stream_gen:
                valid_events.append(event)

            # 应该只有一个有效事件
            assert len(valid_events) == 1
            assert valid_events[0]["event"] == "valid"
            assert valid_events[0]["data"]["answer"] == "正常"

    @patch("aiohttp.ClientSession.request")
    async def test_retry_stream_functionality(self, mock_request, dify_service):
        """测试带重试的流式请求"""

        # 模拟第一次失败，第二次成功
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1

            mock_response = AsyncMock()
            if call_count == 1:
                # 第一次调用失败
                mock_response.status = 500
                mock_response.json = AsyncMock(
                    return_value={"message": "Internal Server Error"}
                )
            else:
                # 第二次调用成功
                mock_response.status = 200
                mock_response.content.iter_chunked = AsyncMock()

                async def mock_chunks():
                    yield 'data: {"event": "message", "data": {"answer": "重试成功"}}\n'.encode(
                        "utf-8"
                    )

                mock_response.content.iter_chunked.return_value = mock_chunks()

            return mock_response.__aenter__.return_value

        mock_request.return_value.__aenter__.side_effect = side_effect

        # 测试带重试的流式请求
        events = []
        async for event in dify_service.send_message_with_retry_stream(
            query="测试重试", user="test_user", max_retries=2, retry_delay=0.1
        ):
            events.append(event)

        assert len(events) == 1
        assert events[0]["data"]["answer"] == "重试成功"
        assert call_count == 2  # 确认进行了重试


# 运行测试的主函数
async def run_integration_tests():
    """运行集成测试"""
    print("开始运行 Dify 流式响应集成测试...")

    # 这里可以添加实际的测试运行逻辑
    # 由于这是一个示例，实际使用时需要配置 pytest 或其他测试框架

    print("所有测试用例:")
    print("✓ test_parse_stream_event - 流式事件解析测试")
    print("✓ test_streaming_request_success - 成功流式请求测试")
    print("✓ test_send_message_stream_mode - 流式消息发送测试")
    print("✓ test_collect_stream_response - 完整响应收集测试")
    print("✓ test_streaming_error_handling - 流式错误处理测试")
    print("✓ test_malformed_sse_handling - 畸形数据处理测试")
    print("✓ test_retry_stream_functionality - 重试机制测试")
    print("\n集成测试框架准备完毕！")
    print("\n运行方法:")
    print("pytest test_streaming_integration.py -v")


if __name__ == "__main__":
    asyncio.run(run_integration_tests())
