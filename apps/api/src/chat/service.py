# 智能问数业务逻辑服务
# 处理自然语言理解、SQL生成、数据查询、图表生成等核心业务逻辑

import logging
from typing import Dict, List, Any
from .chat_service import DifyService
from .schemas import (
    ChatQueryRequest,
    FeedbackRequest,
    ChatHistoryRequest,
    ChatHistoryResponse,
    MessageInfo,
)
from .exceptions import ChatException, ValidationError
from .utils import sanitize_query, format_dify_response, validate_user_id

# 导入配置 - 使用绝对导入
try:
    from core.config import settings
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from core.config import settings

logger = logging.getLogger(__name__)


class ChatService:
    """智能问数服务类 - 业务逻辑协调层"""

    def __init__(self):
        """初始化聊天服务"""
        self.query_dify_service = None
        self.analysis_dify_service = None
        self._initialize_services()

    def _initialize_services(self):
        """初始化 Dify 服务实例"""
        if not settings.dify_base_url or not settings.dify_api_key:
            logger.warning("Dify configuration not complete")
            return

        try:
            # 问数服务
            self.query_dify_service = DifyService(
                base_url=settings.dify_base_url,
                api_key=settings.dify_api_key.get_secret_value(),
                timeout=settings.chat_request_timeout,
            )

            # 分析服务
            if settings.dify_analysis_api_key:
                self.analysis_dify_service = DifyService(
                    base_url=settings.dify_base_url,
                    api_key=settings.dify_analysis_api_key.get_secret_value(),
                    timeout=settings.chat_request_timeout,
                )
            else:
                # 如果没有分析API密钥，使用同一个服务
                self.analysis_dify_service = self.query_dify_service

        except Exception as e:
            logger.error(f"Failed to initialize Dify services: {e}")
            raise ChatException(f"Service initialization failed: {str(e)}")

    async def process_query(self, request: ChatQueryRequest):
        """
        处理智能问数查询

        Args:
            request: 查询请求

        Returns:
            查询响应: Dict (非流式) 或 AsyncGenerator (流式)
        """
        if not self.query_dify_service:
            raise ChatException("Query service not available")

        # 验证输入
        self._validate_request(request)

        # 清理查询内容
        cleaned_query = sanitize_query(request.query)

        try:
            logger.info(f"Processing query: {cleaned_query[:100]}...")

            # 调用 Dify 服务
            response = await self.query_dify_service.send_message(
                query=cleaned_query,
                conversation_id=request.conversation_id,
                inputs=request.inputs,
                stream=request.stream,
                files=request.files,
                user=request.user,
            )

            # 流式响应直接返回生成器
            if request.stream:
                return response

            # 非流式响应格式化后返回
            return format_dify_response(response)

        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            raise ChatException(f"Query processing failed: {str(e)}")

    async def process_analysis(self, request: ChatQueryRequest):
        """
        处理数据分析查询

        Args:
            request: 分析请求

        Returns:
            分析响应: Dict (非流式) 或 AsyncGenerator (流式)
        """
        if not self.analysis_dify_service:
            raise ChatException("Analysis service not available")

        # 验证输入
        self._validate_request(request)

        # 清理查询内容
        cleaned_query = sanitize_query(request.query)

        try:
            logger.info(f"Processing analysis: {cleaned_query[:100]}...")

            # 调用 Dify 分析服务
            response = await self.analysis_dify_service.send_message(
                query=cleaned_query,
                conversation_id=request.conversation_id,
                inputs=request.inputs,
                stream=request.stream,
                files=request.files,
                user=request.user,
            )

            # 流式响应直接返回生成器
            if request.stream:
                return response

            # 非流式响应格式化后返回
            return format_dify_response(response)

        except Exception as e:
            logger.error(f"Analysis processing failed: {e}")
            raise ChatException(f"Analysis processing failed: {str(e)}")

    async def get_history(self, request: ChatHistoryRequest) -> ChatHistoryResponse:
        """
        获取对话历史

        Args:
            request: 历史记录请求

        Returns:
            历史记录响应
        """
        if not self.query_dify_service:
            raise ChatException("Service not available")

        # 验证用户ID
        if not validate_user_id(request.user):
            raise ValidationError("Invalid user ID")

        try:
            logger.info(f"Getting history for user: {request.user}")

            response = await self.query_dify_service.get_messages(
                user=request.user,
                conversation_id=request.conversation_id,
                limit=request.limit,
            )

            # 转换为标准格式
            messages = []
            for msg_data in response.get("data", []):
                message = MessageInfo(**msg_data)
                messages.append(message)

            return ChatHistoryResponse(
                limit=response.get("limit", request.limit),
                has_more=response.get("has_more", False),
                data=messages,
            )

        except Exception as e:
            logger.error(f"Failed to get history: {e}")
            raise ChatException(f"Failed to get history: {str(e)}")

    async def submit_feedback(self, request: FeedbackRequest) -> Dict[str, Any]:
        """
        提交用户反馈

        Args:
            request: 反馈请求

        Returns:
            提交结果
        """
        if not self.query_dify_service:
            raise ChatException("Service not available")

        # 验证输入
        if not validate_user_id(request.user):
            raise ValidationError("Invalid user ID")

        if not request.message_id:
            raise ValidationError("Message ID is required")

        try:
            logger.info(f"Submitting feedback for message: {request.message_id}")

            response = await self.query_dify_service.submit_feedback(
                message_id=request.message_id,
                rating=request.rating,
                user=request.user,
                content=request.content,
            )

            return response

        except Exception as e:
            logger.error(f"Failed to submit feedback: {e}")
            raise ChatException(f"Failed to submit feedback: {str(e)}")

    async def get_suggested_questions(self, message_id: str, user: str) -> List[str]:
        """
        获取建议问题

        Args:
            message_id: 消息ID
            user: 用户ID

        Returns:
            建议问题列表
        """
        if not self.query_dify_service:
            raise ChatException("Service not available")

        # 验证输入
        if not validate_user_id(user):
            raise ValidationError("Invalid user ID")

        if not message_id:
            raise ValidationError("Message ID is required")

        try:
            logger.info(f"Getting suggested questions for message: {message_id}")

            questions = await self.query_dify_service.get_suggested_questions(
                message_id=message_id, user=user
            )

            return questions

        except Exception as e:
            logger.error(f"Failed to get suggested questions: {e}")
            raise ChatException(f"Failed to get suggested questions: {str(e)}")

    def _validate_request(self, request: ChatQueryRequest):
        """验证请求参数"""
        if not request.query or not request.query.strip():
            raise ValidationError("Query cannot be empty")

        if request.user and not validate_user_id(request.user):
            raise ValidationError("Invalid user ID")

        # 查询长度限制
        if len(request.query) > 5000:
            raise ValidationError("Query too long (max 5000 characters)")

    async def close(self):
        """关闭服务连接"""
        try:
            if self.query_dify_service:
                await self.query_dify_service.close()

            if (
                self.analysis_dify_service
                and self.analysis_dify_service != self.query_dify_service
            ):
                await self.analysis_dify_service.close()

        except Exception as e:
            logger.error(f"Error closing services: {e}")


# 全局服务实例
chat_service = ChatService()
