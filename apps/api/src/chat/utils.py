# Chat 模块工具函数
# 包含常用的工具函数和辅助方法

import asyncio
import logging
from typing import Dict, Any, Optional
from functools import wraps
import uuid

logger = logging.getLogger(__name__)


def generate_conversation_id() -> str:
    """生成会话ID"""
    return str(uuid.uuid4())


def generate_message_id() -> str:
    """生成消息ID"""
    return str(uuid.uuid4())


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """异步重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Function {func.__name__} failed after {max_retries} attempts: {e}")
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
            return None
        return wrapper
    return decorator


def sanitize_query(query: str) -> str:
    """清理用户输入查询"""
    if not query:
        return ""

    # 移除多余的空白字符
    query = query.strip()

    # 限制长度
    max_length = 5000
    if len(query) > max_length:
        query = query[:max_length]

    return query


def format_dify_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """格式化 Dify API 响应"""
    return {
        "success": True,
        "conversation_id": response.get("conversation_id"),
        "answer": response.get("answer", ""),
        "message_id": response.get("id"),
        "metadata": response.get("metadata", {}),
        "created_at": response.get("created_at")
    }


def validate_user_id(user_id: str) -> bool:
    """验证用户ID格式"""
    if not user_id or not isinstance(user_id, str):
        return False

    # 简单的格式验证
    if len(user_id.strip()) < 1 or len(user_id) > 100:
        return False

    return True


def log_api_call(endpoint: str, params: Dict[str, Any] = None):
    """记录API调用日志"""
    logger.info(f"API Call: {endpoint}", extra={"params": params or {}})
