# 智能问数相关数据模型
# 定义聊天记录、查询历史等数据库模型

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class ChatSession(Base):
    """聊天会话模型"""

    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    conversation_id = Column(String, unique=True, index=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)


class QueryHistory(Base):
    """查询历史模型"""

    __tablename__ = "query_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    message_id = Column(String, unique=True, index=True)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    query_type = Column(String, default="query")  # query, analysis
    inputs = Column(JSON, default={})
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())
    processing_time = Column(Integer, default=0)  # 处理时间（毫秒）


class Feedback(Base):
    """用户反馈模型"""

    __tablename__ = "feedbacks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    rating = Column(String, nullable=True)  # like, dislike, null
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ApiUsage(Base):
    """API 使用统计模型"""

    __tablename__ = "api_usage"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    processing_time = Column(Integer, default=0)  # 处理时间（毫秒）
    created_at = Column(DateTime, server_default=func.now())
    metadata = Column(JSON, default={})
