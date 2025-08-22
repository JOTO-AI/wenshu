# Dify AI 服务集成
# 封装所有与 Dify API 的交互逻辑

import aiohttp
import asyncio
import logging
import json
from typing import Dict, List, Any, Optional, AsyncGenerator
from .exceptions import DifyServiceException, AuthenticationError, RateLimitError
from .utils import retry_on_failure, log_api_call

logger = logging.getLogger(__name__)


class DifyService:
    """Dify AI 平台服务集成"""

    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        """
        初始化 Dify 服务

        Args:
            base_url: Dify API 基础 URL
            api_key: API 密钥
            timeout: 请求超时时间
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建 HTTP 会话"""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(
                connector=connector, timeout=timeout, headers=self._get_headers()
            )
        return self._session

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """发送HTTP请求（非流式）"""
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()

        log_api_call(f"{method} {endpoint}", {"params": params, "data": data})

        try:
            async with session.request(
                method=method, url=url, json=data, params=params
            ) as response:
                response_data = await response.json()

                if response.status == 401:
                    raise AuthenticationError(
                        "Invalid API key or authentication failed"
                    )
                elif response.status == 429:
                    raise RateLimitError("API rate limit exceeded")
                elif response.status >= 400:
                    error_msg = response_data.get("message", f"HTTP {response.status}")
                    raise DifyServiceException(error_msg, response.status)

                return response_data

        except aiohttp.ClientError as e:
            logger.error(f"Network error calling Dify API: {e}")
            raise DifyServiceException(f"Network error: {str(e)}")

    async def _make_streaming_request(
        self,
        method: str,
        endpoint: str,
        data: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """发送HTTP流式请求"""
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()

        log_api_call(
            f"{method} {endpoint} (streaming)", {"params": params, "data": data}
        )

        try:
            async with session.request(
                method=method, url=url, json=data, params=params
            ) as response:
                if response.status == 401:
                    raise AuthenticationError(
                        "Invalid API key or authentication failed"
                    )
                elif response.status == 429:
                    raise RateLimitError("API rate limit exceeded")
                elif response.status >= 400:
                    try:
                        error_data = await response.json()
                        error_msg = error_data.get("message", f"HTTP {response.status}")
                    except Exception:
                        error_msg = f"HTTP {response.status}"
                    raise DifyServiceException(error_msg, response.status)

                # 处理 Server-Sent Events 流
                buffer = ""
                async for chunk in response.content.iter_chunked(1024):
                    chunk_str = chunk.decode("utf-8", errors="ignore")
                    buffer += chunk_str

                    # 按行分割处理
                    lines = buffer.split("\n")
                    # 保留最后一个不完整的行
                    buffer = lines[-1]

                    for line in lines[:-1]:
                        line = line.strip()

                        # SSE 格式: "data: {...}"
                        if line.startswith("data: "):
                            try:
                                # 移除 "data: " 前缀
                                json_str = line[6:].strip()

                                # 跳过空行和特殊标记
                                if not json_str or json_str == "[DONE]":
                                    continue

                                # 解析 JSON
                                event_data = json.loads(json_str)
                                yield event_data

                            except json.JSONDecodeError as e:
                                logger.warning(
                                    f"Failed to parse SSE data: {json_str}, error: {e}"
                                )
                                continue
                            except Exception as e:
                                logger.error(
                                    f"Error processing SSE line: {line}, error: {e}"
                                )
                                continue
                        # 处理其他 SSE 字段（如 event:, id:, retry: 等）
                        elif line.startswith(("event:", "id:", "retry:")):
                            # 暂时忽略这些字段，但可以在需要时扩展
                            continue

                # 处理缓冲区中剩余的数据
                if buffer.strip():
                    line = buffer.strip()
                    if line.startswith("data: "):
                        try:
                            json_str = line[6:].strip()
                            if json_str and json_str != "[DONE]":
                                event_data = json.loads(json_str)
                                yield event_data
                        except (json.JSONDecodeError, Exception) as e:
                            logger.warning(
                                f"Failed to parse final SSE data: {json_str}, error: {e}"
                            )

        except aiohttp.ClientError as e:
            logger.error(f"Network error calling Dify API: {e}")
            raise DifyServiceException(f"Network error: {str(e)}")

    @retry_on_failure(max_retries=3, delay=1.0)
    async def send_message(
        self,
        query: str,
        conversation_id: Optional[str] = None,
        inputs: Optional[Dict] = None,
        stream: bool = False,
        files: Optional[List[Dict]] = None,
        user: Optional[str] = None,
    ):
        """
        发送消息到 Dify

        Args:
            query: 用户查询
            conversation_id: 会话ID（可选）
            inputs: 额外输入参数
            stream: 是否流式响应
            files: 文件列表
            user: 用户标识

        Returns:
            Dict[str, Any]: 非流式响应时返回完整响应
            AsyncGenerator[Dict[str, Any], None]: 流式响应时返回异步生成器
        """
        payload = {
            "inputs": inputs or {},
            "query": query,
            "response_mode": "streaming" if stream else "blocking",
            "user": user or "default",
        }

        if conversation_id:
            payload["conversation_id"] = conversation_id

        if files:
            payload["files"] = files

        # 根据是否流式选择不同的请求方法
        if stream:
            return self._make_streaming_request("POST", "/chat-messages", payload)
        else:
            return await self._make_request("POST", "/chat-messages", payload)

    async def send_message_stream(
        self,
        query: str,
        conversation_id: Optional[str] = None,
        inputs: Optional[Dict] = None,
        files: Optional[List[Dict]] = None,
        user: Optional[str] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        发送流式消息到 Dify (便捷方法)

        Args:
            query: 用户查询
            conversation_id: 会话ID（可选）
            inputs: 额外输入参数
            files: 文件列表
            user: 用户标识

        Yields:
            Dict[str, Any]: 流式事件数据
        """
        async for event in await self.send_message(
            query=query,
            conversation_id=conversation_id,
            inputs=inputs,
            stream=True,
            files=files,
            user=user,
        ):
            yield event

    @retry_on_failure(max_retries=2, delay=0.5)
    async def submit_feedback(
        self,
        message_id: str,
        rating: Optional[str],
        user: str,
        content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        提交消息反馈

        Args:
            message_id: 消息ID
            rating: 评分 ("like", "dislike", None)
            user: 用户标识
            content: 反馈内容
        """
        payload = {"rating": rating, "user": user}

        if content:
            payload["content"] = content

        endpoint = f"/messages/{message_id}/feedbacks"
        return await self._make_request("POST", endpoint, payload)

    @retry_on_failure(max_retries=2, delay=0.5)
    async def get_messages(
        self, user: str, conversation_id: Optional[str] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """
        获取历史消息

        Args:
            user: 用户标识
            conversation_id: 会话ID
            limit: 返回消息数量限制
        """
        params = {"user": user, "limit": limit}

        if conversation_id:
            params["conversation_id"] = conversation_id

        return await self._make_request("GET", "/messages", params=params)

    @retry_on_failure(max_retries=2, delay=0.5)
    async def get_suggested_questions(self, message_id: str, user: str) -> List[str]:
        """
        获取建议问题

        Args:
            message_id: 消息ID
            user: 用户标识
        """
        params = {"user": user}
        endpoint = f"/messages/{message_id}/suggested"

        response = await self._make_request("GET", endpoint, params=params)
        return response.get("data", [])

    def parse_stream_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析流式事件

        Args:
            event: 原始事件数据

        Returns:
            Dict[str, Any]: 解析后的事件数据，包含事件类型和相关信息
        """
        event_type = event.get("event", "")
        task_id = event.get("task_id", "")
        workflow_run_id = event.get("workflow_run_id", "")
        data = event.get("data", {})

        parsed_event = {
            "event_type": event_type,
            "task_id": task_id,
            "workflow_run_id": workflow_run_id,
            "data": data,
            "raw": event,
        }

        # 根据事件类型添加特定信息
        if event_type == "workflow_started":
            parsed_event.update(
                {
                    "workflow_id": data.get("workflow_id"),
                    "created_at": data.get("created_at"),
                }
            )
        elif event_type in ["node_started", "node_finished"]:
            parsed_event.update(
                {
                    "node_id": data.get("node_id"),
                    "node_type": data.get("node_type"),
                    "title": data.get("title"),
                    "index": data.get("index"),
                    "status": data.get("status"),
                    "elapsed_time": data.get("elapsed_time"),
                }
            )
        elif event_type == "message":
            parsed_event.update(
                {
                    "message_id": data.get("id"),
                    "answer": data.get("answer", ""),
                    "conversation_id": data.get("conversation_id"),
                    "created_at": data.get("created_at"),
                }
            )
        elif event_type == "message_end":
            parsed_event.update(
                {
                    "message_id": data.get("id"),
                    "metadata": data.get("metadata", {}),
                    "usage": data.get("usage", {}),
                }
            )

        return parsed_event

    async def collect_stream_response(
        self, stream_generator: AsyncGenerator[Dict[str, Any], None]
    ) -> Dict[str, Any]:
        """
        收集完整的流式响应

        Args:
            stream_generator: 流式响应生成器

        Returns:
            Dict[str, Any]: 完整响应，包含所有事件和最终结果
        """
        events = []
        final_answer = ""
        conversation_id = None
        message_id = None
        usage = {}
        metadata = {}

        async for event in stream_generator:
            parsed_event = self.parse_stream_event(event)
            events.append(parsed_event)

            # 收集关键信息
            if parsed_event["event_type"] == "message":
                final_answer += parsed_event.get("answer", "")
                if not conversation_id:
                    conversation_id = parsed_event.get("conversation_id")
                if not message_id:
                    message_id = parsed_event.get("message_id")

            elif parsed_event["event_type"] == "message_end":
                usage = parsed_event.get("usage", {})
                metadata = parsed_event.get("metadata", {})
                if not message_id:
                    message_id = parsed_event.get("message_id")

        return {
            "answer": final_answer,
            "conversation_id": conversation_id,
            "message_id": message_id,
            "usage": usage,
            "metadata": metadata,
            "events": events,
            "total_events": len(events),
        }

    async def send_message_with_retry_stream(
        self,
        query: str,
        conversation_id: Optional[str] = None,
        inputs: Optional[Dict] = None,
        files: Optional[List[Dict]] = None,
        user: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        带重试机制的流式消息发送

        Args:
            query: 用户查询
            conversation_id: 会话ID（可选）
            inputs: 额外输入参数
            files: 文件列表
            user: 用户标识
            max_retries: 最大重试次数
            retry_delay: 重试间隔

        Yields:
            Dict[str, Any]: 流式事件数据
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                stream_generator = await self.send_message(
                    query=query,
                    conversation_id=conversation_id,
                    inputs=inputs,
                    stream=True,
                    files=files,
                    user=user,
                )

                # 成功获取流，开始处理事件
                async for event in stream_generator:
                    yield event

                # 如果成功完成，退出重试循环
                return

            except (DifyServiceException, AuthenticationError, RateLimitError) as e:
                last_exception = e
                logger.warning(f"Stream attempt {attempt + 1} failed: {e}")

                # 对于认证错误，不进行重试
                if isinstance(e, AuthenticationError):
                    raise e

                # 对于速率限制，增加重试延迟
                if isinstance(e, RateLimitError):
                    delay = retry_delay * (2**attempt)  # 指数退避
                    logger.info(f"Rate limit hit, waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                else:
                    await asyncio.sleep(retry_delay)

            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error in stream attempt {attempt + 1}: {e}")
                await asyncio.sleep(retry_delay)

        # 所有重试都失败了
        if last_exception:
            raise last_exception
        else:
            raise DifyServiceException(
                "All retry attempts failed for streaming request"
            )

    async def close(self):
        """关闭HTTP会话"""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
