'use client';

import { AssistantRuntimeProvider } from '@assistant-ui/react';
import { useChatRuntime } from '@assistant-ui/react-ai-sdk';
import {
  Button,
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@wenshu/ui';
import { Thread } from '../../../../components/assistant-ui/thread';

export function ChatPage() {
  // 使用真正的 assistant-ui runtime
  // TODO: 实现后端 API 端点 '/api/chat'
  const runtime = useChatRuntime();

  const handleQuickAction = (prompt: string) => {
    // TODO: 实现快速操作功能
    console.log('Quick action:', prompt);
  };

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className='min-h-screen bg-background p-6'>
        <div className='mx-auto max-w-6xl space-y-6'>
          {/* 页面标题和说明 */}
          <div className='text-center space-y-4'>
            <h1 className='text-4xl font-bold tracking-tight'>智能问数助手</h1>
            <p className='text-xl text-muted-foreground max-w-2xl mx-auto'>
              通过自然语言与数据对话，快速获取洞察和可视化结果
            </p>
          </div>

          {/* 功能介绍卡片 */}
          <div className='grid grid-cols-1 md:grid-cols-3 gap-4 mb-8'>
            <Card>
              <CardHeader>
                <CardTitle className='text-lg flex items-center gap-2'>
                  🔍 智能查询
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  使用自然语言描述您的数据需求，AI 自动生成对应的查询语句
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className='text-lg flex items-center gap-2'>
                  📊 数据可视化
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  自动生成各种类型的图表和报表，让数据更直观易懂
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className='text-lg flex items-center gap-2'>
                  ⚡ 实时分析
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  实时处理数据请求，快速响应复杂的分析需求
                </CardDescription>
              </CardContent>
            </Card>
          </div>

          {/* 聊天界面 */}
          <div className='grid grid-cols-1 lg:grid-cols-3 gap-6'>
            {/* 主聊天区域 - 使用真正的 Assistant UI Thread 组件 */}
            <div className='lg:col-span-2 h-[600px]'>
              <Thread
                welcome={{
                  suggestions: [
                    { prompt: '显示今日用户活动统计' },
                    { prompt: '生成用户增长趋势图表' },
                    { prompt: '查询系统性能指标' },
                    { prompt: '导出月度数据报表' },
                  ],
                }}
                className='h-full border rounded-lg'
              />
            </div>

            {/* 侧边栏 - 快速操作 */}
            <div className='space-y-4'>
              <Card>
                <CardHeader>
                  <CardTitle>快速操作</CardTitle>
                  <CardDescription>常用的数据查询和分析操作</CardDescription>
                </CardHeader>
                <CardContent className='space-y-3'>
                  <Button
                    variant='outline'
                    className='w-full justify-start'
                    onClick={() => handleQuickAction('显示今日用户活动统计')}
                  >
                    📈 今日活动统计
                  </Button>
                  <Button
                    variant='outline'
                    className='w-full justify-start'
                    onClick={() => handleQuickAction('生成用户增长趋势图表')}
                  >
                    📊 用户增长趋势
                  </Button>
                  <Button
                    variant='outline'
                    className='w-full justify-start'
                    onClick={() => handleQuickAction('查询系统性能指标')}
                  >
                    ⚡系统性能指标
                  </Button>
                  <Button
                    variant='outline'
                    className='w-full justify-start'
                    onClick={() => handleQuickAction('导出月度数据报表')}
                  >
                    📑 导出数据报表
                  </Button>
                </CardContent>
              </Card>

              {/* 使用提示 */}
              <Card>
                <CardHeader>
                  <CardTitle className='text-sm'>💡 使用提示</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className='text-sm text-muted-foreground space-y-2'>
                    <li>• 尽量用自然语言描述您的需求</li>
                    <li>• 可以要求生成特定类型的图表</li>
                    <li>• 支持复杂的数据分析查询</li>
                    <li>• 可以要求解释数据背后的含义</li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* 底部信息 */}
          <div className='text-center text-sm text-muted-foreground mt-8'>
            <p>
              智能问数系统 - 让数据分析变得简单直观 | 支持自然语言查询 •
              实时数据可视化 • 智能分析建议
            </p>
          </div>
        </div>
      </div>
    </AssistantRuntimeProvider>
  );
}
