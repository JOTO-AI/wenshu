# 智能问数相关数据模式
# 定义聊天查询请求和响应的Pydantic模式

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional


class ChatQueryRequest(BaseModel):
    """聊天查询请求模式"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "What are the specs of the iPhone 13 Pro Max?",
                "inputs": {},
                "stream": True,
                "conversation_id": "",
                "user": "abc-123",
                "files": [
                    {
                        "type": "image",
                        "transfer_method": "remote_url",
                        "url": "https://example.com/image.png",
                    }
                ],
            }
        }
    )

    query: str = Field(
        ..., description="用户输入/提问内容", min_length=1, max_length=5000
    )
    conversation_id: Optional[str] = Field(None, description="会话ID（首次对话不需要）")
    inputs: Optional[Dict[str, Any]] = Field(default={}, description="额外的输入参数")
    stream: Optional[bool] = Field(default=False, description="是否使用流式响应")
    files: Optional[List[Dict]] = Field(None, description="文件列表")
    user: Optional[str] = Field(None, description="用户标识", max_length=100)


class ChartConfig(BaseModel):
    """图表配置模式"""

    type: str = Field(..., description="图表类型：line, bar, pie等")
    data: Dict[str, Any] = Field(..., description="图表数据")
    options: Dict[str, Any] = Field(..., description="图表选项")
    title: Optional[str] = Field(None, description="图表标题")
    width: Optional[int] = Field(None, description="图表宽度")
    height: Optional[int] = Field(None, description="图表高度")


class ChatQueryResponse(BaseModel):
    """聊天查询响应模式"""

    success: bool = Field(..., description="请求是否成功")
    conversation_id: Optional[str] = Field(None, description="会话ID")
    answer: str = Field(..., description="回答内容")
    message_id: Optional[str] = Field(None, description="消息ID")
    metadata: Dict[str, Any] = Field(default={}, description="元数据")
    created_at: Optional[int] = Field(None, description="创建时间戳")


class FeedbackRequest(BaseModel):
    """反馈请求模式"""

    message_id: str = Field(..., description="消息ID")
    rating: Optional[str] = Field(None, description="评分：like/dislike/null")
    user: str = Field(..., description="用户标识", max_length=100)
    content: Optional[str] = Field(None, description="反馈内容", max_length=1000)


class ChatHistoryRequest(BaseModel):
    """历史记录请求模式"""

    user: str = Field(..., description="用户标识", max_length=100)
    conversation_id: Optional[str] = Field(None, description="会话ID")
    limit: int = Field(20, description="返回消息数量限制", ge=1, le=100)


class MessageInfo(BaseModel):
    """消息信息模式"""

    id: str = Field(..., description="消息ID")
    conversation_id: str = Field(..., description="会话ID")
    inputs: Dict[str, Any] = Field(default={}, description="输入参数")
    query: str = Field(..., description="用户查询")
    answer: str = Field(..., description="回答内容")
    message_files: List[Dict] = Field(default=[], description="消息文件")
    feedback: Optional[Dict] = Field(None, description="反馈信息")
    retriever_resources: List[Dict] = Field(default=[], description="检索资源")
    created_at: int = Field(..., description="创建时间戳")


class ChatHistoryResponse(BaseModel):
    """历史记录响应模式"""

    limit: int = Field(..., description="限制数量")
    has_more: bool = Field(..., description="是否有更多数据")
    data: List[MessageInfo] = Field(..., description="消息列表")


class SuggestedQuestionsRequest(BaseModel):
    """建议问题请求模式"""

    message_id: str = Field(..., description="消息ID")
    user: str = Field(..., description="用户标识", max_length=100)


class ErrorResponse(BaseModel):
    """错误响应模式"""

    success: bool = Field(False, description="请求是否成功")
    error: str = Field(..., description="错误信息")
    code: Optional[str] = Field(None, description="错误代码")
    detail: Optional[Dict[str, Any]] = Field(None, description="错误详情")
