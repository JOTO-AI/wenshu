import {
  AssistantRuntimeProvider,
  ThreadPrimitive,
  useLocalRuntime,
} from '@assistant-ui/react';
import {
  Alert,
  AlertDescription,
  Badge,
  Button,
  Card,
  Input,
} from '@workspace/ui';

export default function TestUIPage() {
  const runtime = useLocalRuntime({
    async run({ messages }) {
      // 模拟 API 调用
      await new Promise(resolve => setTimeout(resolve, 1000));
      return {
        content: [
          {
            type: 'text',
            text: `这是对消息的回复`,
          },
        ],
      };
    },
  });

  return (
    <div className='min-h-screen bg-background p-8 space-y-8'>
      {/* 页面标题 */}
      <div className='text-center space-y-4'>
        <h1 className='text-4xl font-bold text-foreground'>UI 组件测试页面</h1>
        <p className='text-muted-foreground'>
          测试 Tailwind CSS、shadcn-ui 和 Assistant UI 组件
        </p>
      </div>

      {/* Tailwind CSS 基础样式测试 */}
      <Card className='p-6'>
        <h2 className='text-2xl font-semibold mb-4 text-primary'>
          Tailwind CSS 基础样式测试
        </h2>
        <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
          {/* 颜色测试 */}
          <div className='space-y-2'>
            <h3 className='font-medium'>颜色系统</h3>
            <div className='flex space-x-2'>
              <div className='w-8 h-8 bg-primary rounded'></div>
              <div className='w-8 h-8 bg-secondary rounded'></div>
              <div className='w-8 h-8 bg-accent rounded'></div>
              <div className='w-8 h-8 bg-muted rounded'></div>
            </div>
          </div>

          {/* 间距测试 */}
          <div className='space-y-2'>
            <h3 className='font-medium'>间距系统</h3>
            <div className='space-y-1'>
              <div className='h-2 bg-primary/20 rounded'></div>
              <div className='h-4 bg-primary/40 rounded'></div>
              <div className='h-6 bg-primary/60 rounded'></div>
              <div className='h-8 bg-primary/80 rounded'></div>
            </div>
          </div>

          {/* 边框测试 */}
          <div className='space-y-2'>
            <h3 className='font-medium'>边框系统</h3>
            <div className='space-y-2'>
              <div className='p-2 border border-border rounded-sm'>border</div>
              <div className='p-2 border-2 border-primary rounded-md'>
                border-2
              </div>
              <div className='p-2 border-4 border-accent rounded-lg'>
                border-4
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* shadcn-ui 组件测试 */}
      <Card className='p-6'>
        <h2 className='text-2xl font-semibold mb-4 text-primary'>
          shadcn-ui 组件测试
        </h2>
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
          {/* 按钮组件 */}
          <div className='space-y-3'>
            <h3 className='font-medium'>按钮组件</h3>
            <div className='space-y-2'>
              <Button variant='default'>默认按钮</Button>
              <Button variant='secondary'>次要按钮</Button>
              <Button variant='outline'>轮廓按钮</Button>
              <Button variant='destructive'>危险按钮</Button>
            </div>
          </div>

          {/* 输入组件 */}
          <div className='space-y-3'>
            <h3 className='font-medium'>输入组件</h3>
            <div className='space-y-2'>
              <Input placeholder='普通输入框' />
              <Input type='email' placeholder='邮箱输入框' />
              <Input type='password' placeholder='密码输入框' />
            </div>
          </div>

          {/* 徽章组件 */}
          <div className='space-y-3'>
            <h3 className='font-medium'>徽章组件</h3>
            <div className='flex flex-wrap gap-2'>
              <Badge variant='default'>默认</Badge>
              <Badge variant='secondary'>次要</Badge>
              <Badge variant='outline'>轮廓</Badge>
              <Badge variant='destructive'>危险</Badge>
            </div>
          </div>
        </div>

        {/* 警告组件 */}
        <div className='mt-6'>
          <h3 className='font-medium mb-3'>警告组件</h3>
          <Alert>
            <AlertDescription>
              这是一个测试警告消息，用于验证 Alert 组件是否正常工作。
            </AlertDescription>
          </Alert>
        </div>
      </Card>

      {/* Assistant UI 组件测试 */}
      <Card className='p-6'>
        <h2 className='text-2xl font-semibold mb-4 text-primary'>
          Assistant UI 组件测试
        </h2>
        <div className='h-96 border border-border rounded-lg overflow-hidden'>
          <AssistantRuntimeProvider runtime={runtime}>
            <ThreadPrimitive.Root className='h-full'>
              <ThreadPrimitive.Viewport className='h-full p-4'>
                <ThreadPrimitive.Empty>
                  <div className='text-center text-muted-foreground'>
                    <p>开始对话...</p>
                    <div className='mt-4 space-y-2'>
                      <ThreadPrimitive.Suggestion
                        prompt='测试消息 1'
                        method='replace'
                        autoSend
                        className='block w-full p-2 text-left border rounded hover:bg-muted'
                      >
                        测试消息 1
                      </ThreadPrimitive.Suggestion>
                      <ThreadPrimitive.Suggestion
                        prompt='测试消息 2'
                        method='replace'
                        autoSend
                        className='block w-full p-2 text-left border rounded hover:bg-muted'
                      >
                        测试消息 2
                      </ThreadPrimitive.Suggestion>
                    </div>
                  </div>
                </ThreadPrimitive.Empty>
                <ThreadPrimitive.Messages
                  components={{
                    UserMessage: () => (
                      <div className='mb-4 p-3 bg-primary/10 rounded-lg'>
                        <div className='font-medium text-primary mb-1'>
                          用户
                        </div>
                        <div>用户消息内容</div>
                      </div>
                    ),
                    AssistantMessage: () => (
                      <div className='mb-4 p-3 bg-muted rounded-lg'>
                        <div className='font-medium text-foreground mb-1'>
                          助手
                        </div>
                        <div>助手回复内容</div>
                      </div>
                    ),
                  }}
                />
              </ThreadPrimitive.Viewport>
            </ThreadPrimitive.Root>
          </AssistantRuntimeProvider>
        </div>
      </Card>

      {/* 响应式测试 */}
      <Card className='p-6'>
        <h2 className='text-2xl font-semibold mb-4 text-primary'>
          响应式布局测试
        </h2>
        <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4'>
          {Array.from({ length: 8 }, (_, i) => (
            <div key={i} className='p-4 bg-muted rounded-lg text-center'>
              <div className='text-sm text-muted-foreground'>
                网格项 {i + 1}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* 状态指示器 */}
      <Card className='p-6'>
        <h2 className='text-2xl font-semibold mb-4 text-primary'>
          样式状态检查
        </h2>
        <div className='space-y-4'>
          <div className='flex items-center space-x-4'>
            <div className='w-4 h-4 bg-green-500 rounded-full'></div>
            <span>如果看到绿色圆点，说明基础 Tailwind 类正常工作</span>
          </div>
          <div className='flex items-center space-x-4'>
            <div className='w-4 h-4 bg-primary rounded-full'></div>
            <span>如果看到主色调圆点，说明 CSS 变量正常工作</span>
          </div>
          <div className='flex items-center space-x-4'>
            <Button size='sm'>小按钮</Button>
            <span>如果按钮样式正常，说明 shadcn-ui 组件正常工作</span>
          </div>
        </div>
      </Card>
    </div>
  );
}
