#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dify 流式响应使用示例
演示如何使用优化后的 DifyService 处理流式和非流式响应
"""

import asyncio
import logging
from .chat_service import DifyService

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_streaming_chat():
    """流式聊天示例"""
    
    # 初始化 Dify 服务
    dify_service = DifyService(
        base_url="https://dify.jototech.cn/v1",
        api_key="your-api-key-here",
        timeout=30
    )
    
    try:
        print("=== 流式聊天示例 ===")
        
        # 方法1: 使用 send_message 方法（stream=True）
        print("\n方法1: 逐个处理流式事件")
        stream_generator = await dify_service.send_message(
            query="你好，请介绍一下你自己",
            stream=True,
            user="test_user"
        )
        
        conversation_id = None
        full_answer = ""
        
        async for event in stream_generator:
            parsed_event = dify_service.parse_stream_event(event)
            event_type = parsed_event["event_type"]
            
            print(f"事件类型: {event_type}")
            
            if event_type == "workflow_started":
                print(f"  工作流开始: {parsed_event.get('workflow_id')}")
                
            elif event_type == "node_started":
                print(f"  节点开始: {parsed_event.get('title')} ({parsed_event.get('node_type')})")
                
            elif event_type == "node_finished":
                print(f"  节点完成: {parsed_event.get('title')}, 耗时: {parsed_event.get('elapsed_time')}s")
                
            elif event_type == "message":
                answer_part = parsed_event.get("answer", "")
                full_answer += answer_part
                print(f"  消息片段: {answer_part}")
                conversation_id = parsed_event.get("conversation_id")
                
            elif event_type == "message_end":
                usage = parsed_event.get("usage", {})
                print(f"  消息结束，使用情况: {usage}")
        
        print(f"\n完整回答: {full_answer}")
        print(f"会话ID: {conversation_id}")
        
        # 方法2: 使用便捷方法收集完整响应
        print("\n方法2: 收集完整流式响应")
        stream_generator2 = await dify_service.send_message(
            query="请告诉我今天的日期",
            conversation_id=conversation_id,  # 继续之前的对话
            stream=True,
            user="test_user"
        )
        
        # 收集完整响应
        complete_response = await dify_service.collect_stream_response(stream_generator2)
        
        print(f"完整回答: {complete_response['answer']}")
        print(f"消息ID: {complete_response['message_id']}")
        print(f"总事件数: {complete_response['total_events']}")
        print(f"使用情况: {complete_response['usage']}")
        
        # 方法3: 使用专用的流式方法
        print("\n方法3: 使用 send_message_stream 方法")
        async for event in dify_service.send_message_stream(
            query="用一句话总结前面的对话",
            conversation_id=conversation_id,
            user="test_user"
        ):
            parsed_event = dify_service.parse_stream_event(event)
            if parsed_event["event_type"] == "message":
                print(f"流式回答: {parsed_event.get('answer', '')}", end="")
        
        print()  # 换行
        
    except Exception as e:
        logger.error(f"流式聊天示例失败: {e}")
    finally:
        await dify_service.close()


async def example_blocking_chat():
    """非流式聊天示例"""
    
    dify_service = DifyService(
        base_url="https://dify.jototech.cn/v1",
        api_key="your-api-key-here",
        timeout=30
    )
    
    try:
        print("\n=== 非流式聊天示例 ===")
        
        response = await dify_service.send_message(
            query="请简短介绍一下人工智能",
            stream=False,  # 非流式
            user="test_user"
        )
        
        print(f"完整回答: {response.get('answer', '')}")
        print(f"消息ID: {response.get('id')}")
        print(f"会话ID: {response.get('conversation_id')}")
        
    except Exception as e:
        logger.error(f"非流式聊天示例失败: {e}")
    finally:
        await dify_service.close()


async def example_event_filtering():
    """事件过滤示例"""
    
    dify_service = DifyService(
        base_url="https://dify.jototech.cn/v1",
        api_key="your-api-key-here",
        timeout=30
    )
    
    try:
        print("\n=== 事件过滤示例 ===")
        
        stream_generator = await dify_service.send_message(
            query="解释一下机器学习的基本概念",
            stream=True,
            user="test_user"
        )
        
        # 只处理消息相关的事件
        full_answer = ""
        async for event in stream_generator:
            parsed_event = dify_service.parse_stream_event(event)
            
            # 只关注消息事件
            if parsed_event["event_type"] == "message":
                answer_part = parsed_event.get("answer", "")
                full_answer += answer_part
                print(answer_part, end="", flush=True)
            elif parsed_event["event_type"] == "message_end":
                usage = parsed_event.get("usage", {})
                print(f"\n\n[使用情况: {usage}]")
        
    except Exception as e:
        logger.error(f"事件过滤示例失败: {e}")
    finally:
        await dify_service.close()


if __name__ == "__main__":
    async def main():
        await example_streaming_chat()
        await example_blocking_chat()
        await example_event_filtering()
    
    # 运行示例
    asyncio.run(main())
