# 智能问数API路由
# 处理聊天查询、SQL生成、图表生成等API端点

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Optional, List, AsyncGenerator
import logging
import json

from .schemas import (
    ChatQueryRequest, ChatQueryResponse, FeedbackRequest,
    ChatHistoryRequest, ChatHistoryResponse, ErrorResponse
)
from .service import chat_service
from .exceptions import ChatException, ValidationError, DifyServiceException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["智能问数"])


async def format_streaming_response(stream_generator: AsyncGenerator) -> AsyncGenerator[str, None]:
    """格式化流式响应为SSE格式"""
    async for event in stream_generator:
        # 将事件转换为JSON字符串并按SSE格式输出
        event_json = json.dumps(event, ensure_ascii=False)
        yield f"data: {event_json}\n\n"
    
    # 发送结束标记
    yield "data: [DONE]\n\n"


@router.post("/query",
    summary="智能问数查询",
    description="发送自然语言查询，获取数据分析结果"
)
async def chat_query(request: ChatQueryRequest):
    """智能问数查询"""
    try:
        logger.info(f"Received query request from user: {request.user}")
        result = await chat_service.process_query(request)
        
        # 处理流式响应
        if request.stream:
            return StreamingResponse(
                format_streaming_response(result),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                }
            )
        
        # 非流式响应
        return result

    except ValidationError as e:
        logger.warning(f"Validation error: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)

    except DifyServiceException as e:
        logger.error(f"Dify service error: {e.message}")
        status_code = e.status_code or 500
        raise HTTPException(status_code=status_code, detail=e.message)

    except ChatException as e:
        logger.error(f"Chat service error: {e.message}")
        raise HTTPException(status_code=500, detail=e.message)

    except Exception as e:
        logger.error(f"Unexpected error in query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/analyze",
    summary="数据分析查询",
    description="发送分析请求，获取深度数据分析结果"
)
async def chat_analyze(request: ChatQueryRequest):
    """数据分析查询"""
    try:
        logger.info(f"Received analysis request from user: {request.user}")
        result = await chat_service.process_analysis(request)
        
        # 处理流式响应
        if request.stream:
            return StreamingResponse(
                format_streaming_response(result),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                }
            )
        
        # 非流式响应
        return result

    except ValidationError as e:
        logger.warning(f"Validation error: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)

    except DifyServiceException as e:
        logger.error(f"Dify service error: {e.message}")
        status_code = e.status_code or 500
        raise HTTPException(status_code=status_code, detail=e.message)

    except ChatException as e:
        logger.error(f"Chat service error: {e.message}")
        raise HTTPException(status_code=500, detail=e.message)

    except Exception as e:
        logger.error(f"Unexpected error in analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history",
    response_model=ChatHistoryResponse,
    summary="获取对话历史",
    description="获取用户的历史对话记录"
)
async def get_history(
    user: str = Query(..., description="用户标识"),
    conversation_id: Optional[str] = Query(None, description="会话ID"),
    limit: int = Query(20, description="返回消息数量限制", ge=1, le=100)
):
    """获取对话历史"""
    try:
        request = ChatHistoryRequest(
            user=user,
            conversation_id=conversation_id,
            limit=limit
        )

        logger.info(f"Getting history for user: {user}")
        result = await chat_service.get_history(request)
        return result

    except ValidationError as e:
        logger.warning(f"Validation error: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)

    except ChatException as e:
        logger.error(f"Chat service error: {e.message}")
        raise HTTPException(status_code=500, detail=e.message)

    except Exception as e:
        logger.error(f"Unexpected error in get_history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/feedback",
    summary="提交消息反馈",
    description="对指定消息进行点赞/点踩反馈"
)
async def submit_feedback(request: FeedbackRequest):
    """提交消息反馈"""
    try:
        logger.info(f"Received feedback from user: {request.user} for message: {request.message_id}")
        result = await chat_service.submit_feedback(request)
        return {"success": True, "message": "Feedback submitted successfully"}

    except ValidationError as e:
        logger.warning(f"Validation error: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)

    except DifyServiceException as e:
        logger.error(f"Dify service error: {e.message}")
        status_code = e.status_code or 500
        raise HTTPException(status_code=status_code, detail=e.message)

    except ChatException as e:
        logger.error(f"Chat service error: {e.message}")
        raise HTTPException(status_code=500, detail=e.message)

    except Exception as e:
        logger.error(f"Unexpected error in submit_feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/suggested/{message_id}",
    response_model=List[str],
    summary="获取建议问题",
    description="获取基于指定消息的建议问题列表"
)
async def get_suggested_questions(
    message_id: str,
    user: str = Query(..., description="用户标识")
):
    """获取建议问题"""
    try:
        logger.info(f"Getting suggested questions for message: {message_id}")
        result = await chat_service.get_suggested_questions(message_id, user)
        return result

    except ValidationError as e:
        logger.warning(f"Validation error: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)

    except DifyServiceException as e:
        logger.error(f"Dify service error: {e.message}")
        status_code = e.status_code or 500
        raise HTTPException(status_code=status_code, detail=e.message)

    except ChatException as e:
        logger.error(f"Chat service error: {e.message}")
        raise HTTPException(status_code=500, detail=e.message)

    except Exception as e:
        logger.error(f"Unexpected error in get_suggested_questions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# 健康检查端点
@router.get("/health",
    summary="健康检查",
    description="检查Chat模块服务状态"
)
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "chat-service",
        "version": "1.0.0"
    }
