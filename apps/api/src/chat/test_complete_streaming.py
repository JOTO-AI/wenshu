"""
完整的流式响应集成测试
测试从 router -> service -> chat_service 的完整流程
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_streaming_query():
    """测试流式查询端点"""
    url = "http://localhost:8000/chat/query"
    
    payload = {
        "query": "分析销售数据趋势",
        "user": "test_user_001",
        "stream": True,
        "inputs": {},
        "conversation_id": None,
        "files": None
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    
    logger.info("开始流式查询测试...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                logger.info(f"响应状态: {response.status}")
                logger.info(f"响应头: {dict(response.headers)}")
                
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"请求失败: {error_text}")
                    return
                
                # 读取流式响应
                event_count = 0
                full_answer = ""
                
                async for line in response.content:
                    line_str = line.decode('utf-8').strip()
                    
                    if not line_str:
                        continue
                        
                    logger.info(f"收到行: {line_str}")
                    
                    # 解析 SSE 格式
                    if line_str.startswith('data: '):
                        data_str = line_str[6:].strip()
                        
                        if data_str == '[DONE]':
                            logger.info("流式响应结束")
                            break
                            
                        try:
                            event_data = json.loads(data_str)
                            event_count += 1
                            
                            logger.info(f"事件 {event_count}: {event_data.get('event', 'unknown')}")
                            
                            # 收集答案内容
                            if event_data.get("event") == "message":
                                answer_part = event_data.get("data", {}).get("answer", "")
                                full_answer += answer_part
                                if answer_part:
                                    logger.info(f"答案片段: {answer_part}")
                                    
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON解析错误: {e}, 数据: {data_str}")
                
                logger.info(f"总共收到 {event_count} 个事件")
                logger.info(f"完整答案: {full_answer}")
                
    except Exception as e:
        logger.error(f"测试失败: {e}")


async def test_non_streaming_query():
    """测试非流式查询端点"""
    url = "http://localhost:8000/chat/query"
    
    payload = {
        "query": "分析销售数据趋势",
        "user": "test_user_002",
        "stream": False,
        "inputs": {},
        "conversation_id": None,
        "files": None
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    logger.info("开始非流式查询测试...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                logger.info(f"响应状态: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"响应结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
                else:
                    error_text = await response.text()
                    logger.error(f"请求失败: {error_text}")
                    
    except Exception as e:
        logger.error(f"测试失败: {e}")


async def test_streaming_analysis():
    """测试流式分析端点"""
    url = "http://localhost:8000/chat/analyze"
    
    payload = {
        "query": "深度分析用户行为数据",
        "user": "test_user_003",
        "stream": True,
        "inputs": {},
        "conversation_id": None,
        "files": None
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    
    logger.info("开始流式分析测试...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                logger.info(f"响应状态: {response.status}")
                
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"请求失败: {error_text}")
                    return
                
                # 读取流式响应
                event_count = 0
                
                async for line in response.content:
                    line_str = line.decode('utf-8').strip()
                    
                    if not line_str:
                        continue
                        
                    if line_str.startswith('data: '):
                        data_str = line_str[6:].strip()
                        
                        if data_str == '[DONE]':
                            logger.info("流式分析响应结束")
                            break
                            
                        try:
                            event_data = json.loads(data_str)
                            event_count += 1
                            logger.info(f"分析事件 {event_count}: {event_data.get('event', 'unknown')}")
                            
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON解析错误: {e}")
                
                logger.info(f"分析总共收到 {event_count} 个事件")
                
    except Exception as e:
        logger.error(f"分析测试失败: {e}")


async def main():
    """运行所有测试"""
    logger.info("开始完整的流式响应集成测试")
    
    # 测试流式查询
    await test_streaming_query()
    
    await asyncio.sleep(2)  # 等待2秒
    
    # 测试非流式查询
    await test_non_streaming_query()
    
    await asyncio.sleep(2)  # 等待2秒
    
    # 测试流式分析
    await test_streaming_analysis()
    
    logger.info("所有测试完成")


if __name__ == "__main__":
    asyncio.run(main())
