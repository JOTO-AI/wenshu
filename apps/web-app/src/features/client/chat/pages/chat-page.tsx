'use client';

import { AssistantRuntimeProvider } from '@assistant-ui/react';
import { useChatRuntime } from '@assistant-ui/react-ai-sdk';
import { Thread } from '../../../../components/assistant-ui/thread';

export function ChatPage() {
  // 使用真正的 assistant-ui runtime
  // TODO: 实现后端 API 端点 '/api/chat'
  const runtime = useChatRuntime();

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className='flex h-screen bg-background'>
        {/* 主聊天区域 - 全屏对话体验 */}
        <div className='flex-1 flex flex-col'>
          <Thread
            welcome={{
              suggestions: [
                { prompt: '显示今日用户活动统计' },
                { prompt: '生成用户增长趋势图表' },
                { prompt: '查询系统性能指标' },
                { prompt: '导出月度数据报表' },
                { prompt: '分析用户行为模式' },
                { prompt: '创建销售业绩仪表板' },
              ],
            }}
            className='flex-1'
          />
        </div>
      </div>
    </AssistantRuntimeProvider>
  );
}
