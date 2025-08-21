#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 Dify 流式响应功能
"""

import asyncio
import os
import logging
from typing import Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_streaming():
    """测试流式响应功能"""
    from .chat_service import DifyService
    
    # 从环境变量读取配置
    base_url = os.getenv("DIFY_BASE_URL", "https://dify.jototech.cn/v1")
    api_key = os.getenv("DIFY_API_KEY")
    
    if not api_key:
        logger.error("请设置环境变量 DIFY_API_KEY")
        return
    
    dify_service = DifyService(
        base_url=base_url,
        api_key=api_key,
        timeout=30
    )
    
    try:
        logger.info("开始测试流式响应...")
        
        # 测试流式响应
        stream_generator = await dify_service.send_message(
            query="你好，请简单介绍一下自己",
            stream=True,
            user="test_user"
        )
        
        logger.info("接收流式事件:")
        events_count = 0
        message_parts = []
        
        async for event in stream_generator:
            events_count += 1
            parsed_event = dify_service.parse_stream_event(event)
            event_type = parsed_event["event_type"]
            
            logger.info(f"事件 {events_count}: {event_type}")
            
            if event_type == "message":
                answer_part = parsed_event.get("answer", "")
                if answer_part:
                    message_parts.append(answer_part)
                    print(answer_part, end="", flush=True)
            elif event_type == "message_end":
                usage = parsed_event.get("usage", {})
                logger.info(f"消息结束，使用情况: {usage}")
                print()  # 换行
        
        full_message = "".join(message_parts)
        logger.info(f"总事件数: {events_count}")
        logger.info(f"完整消息长度: {len(full_message)}")
        logger.info("流式响应测试成功！")
        
    except Exception as e:
        logger.error(f"流式响应测试失败: {e}", exc_info=True)
    finally:
        await dify_service.close()


async def test_non_streaming():
    """测试非流式响应功能"""
    from .chat_service import DifyService
    
    # 从环境变量读取配置
    base_url = os.getenv("DIFY_BASE_URL", "https://dify.jototech.cn/v1")
    api_key = os.getenv("DIFY_API_KEY")
    
    if not api_key:
        logger.error("请设置环境变量 DIFY_API_KEY")
        return
    
    dify_service = DifyService(
        base_url=base_url,
        api_key=api_key,
        timeout=30
    )
    
    try:
        logger.info("开始测试非流式响应...")
        
        response = await dify_service.send_message(
            query="用一句话介绍人工智能",
            stream=False,  # 非流式
            user="test_user"
        )
        
        logger.info(f"响应ID: {response.get('id', 'N/A')}")
        logger.info(f"会话ID: {response.get('conversation_id', 'N/A')}")
        logger.info(f"回答: {response.get('answer', 'N/A')}")
        logger.info("非流式响应测试成功！")
        
    except Exception as e:
        logger.error(f"非流式响应测试失败: {e}", exc_info=True)
    finally:
        await dify_service.close()


if __name__ == "__main__":
    async def main():
        print("=== Dify 服务测试 ===\n")
        
        # 测试流式响应
        await test_streaming()
        
        print("\n" + "="*50 + "\n")
        
        # 测试非流式响应
        await test_non_streaming()
        
        print("\n测试完成！")
    
    # 运行测试
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        logger.error(f"测试运行失败: {e}", exc_info=True)
