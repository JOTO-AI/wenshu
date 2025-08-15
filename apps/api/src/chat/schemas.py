# 智能问数相关数据模式
# 定义聊天查询请求和响应的Pydantic模式

from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ChatQueryRequest(BaseModel):
    """聊天查询请求模式"""
    query: str
    session_id: Optional[str] = None


class ChartConfig(BaseModel):
    """图表配置模式"""
    type: str  # 图表类型：line, bar, pie等
    data: Dict[str, Any]
    options: Dict[str, Any]


class ChatQueryResponse(BaseModel):
    """聊天查询响应模式"""
    query: str
    sql: Optional[str] = None
    data: List[Dict[str, Any]]
    chart: Optional[ChartConfig] = None
    explanation: str
    session_id: str


class FeedbackRequest(BaseModel):
    """反馈请求模式"""
    query_id: str
    feedback_type: str  # like, dislike
    comment: Optional[str] = None