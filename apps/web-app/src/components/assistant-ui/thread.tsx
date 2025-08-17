import {
  ComposerPrimitive,
  MessagePrimitive,
  ThreadPrimitive,
} from '@assistant-ui/react';
import { Button, cn } from '@wenshu/ui';
import type { FC } from 'react';

interface ThreadProps {
  className?: string;
  welcome?: {
    suggestions?: Array<{ prompt: string }>;
  };
}

export const Thread: FC<ThreadProps> = ({ className, welcome }) => {
  return (
    <ThreadPrimitive.Root className={cn('aui-root aui-thread-root', className)}>
      <ThreadPrimitive.Viewport className='flex-1 overflow-y-auto px-4 pt-8'>
        <ThreadWelcome welcome={welcome} />
        <ThreadMessages />
        <ThreadScrollToBottom />
      </ThreadPrimitive.Viewport>
      <ThreadComposer />
    </ThreadPrimitive.Root>
  );
};

const ThreadWelcome: FC<{ welcome?: ThreadProps['welcome'] }> = ({
  welcome,
}) => {
  return (
    <ThreadPrimitive.Empty>
      <div className='flex flex-col items-center justify-center h-full space-y-6 text-center'>
        <div className='space-y-2'>
          <h2 className='text-2xl font-semibold'>欢迎使用智能问数助手</h2>
          <p className='text-muted-foreground'>
            开始对话，我可以帮助您分析数据、生成图表和回答问题
          </p>
        </div>

        {welcome?.suggestions && (
          <div className='grid grid-cols-1 md:grid-cols-2 gap-2 w-full max-w-2xl'>
            {welcome.suggestions.map((suggestion, index) => (
              <ThreadPrimitive.Suggestion
                key={index}
                prompt={suggestion.prompt}
                method='replace'
                asChild
              >
                <Button
                  variant='outline'
                  className='h-auto p-3 whitespace-normal text-left justify-start'
                >
                  {suggestion.prompt}
                </Button>
              </ThreadPrimitive.Suggestion>
            ))}
          </div>
        )}
      </div>
    </ThreadPrimitive.Empty>
  );
};

const ThreadMessages: FC = () => {
  return (
    <ThreadPrimitive.Messages
      components={{
        UserMessage,
        AssistantMessage,
      }}
    />
  );
};

const ThreadScrollToBottom: FC = () => {
  return (
    <ThreadPrimitive.ScrollToBottom asChild>
      <Button
        variant='outline'
        size='icon'
        className='aui-thread-scroll-to-bottom'
      >
        ↓
      </Button>
    </ThreadPrimitive.ScrollToBottom>
  );
};

const ThreadComposer: FC = () => {
  return (
    <ThreadPrimitive.If running={false}>
      <ComposerPrimitive.Root className='flex w-full items-end gap-2 rounded-lg border p-2'>
        <ComposerPrimitive.Input
          autoFocus
          placeholder='输入您的问题...'
          className='flex-1 resize-none border-0 bg-transparent px-2 py-1.5 text-sm outline-none placeholder:text-muted-foreground'
        />
        <ComposerPrimitive.Send asChild>
          <Button size='icon' className='size-8'>
            →
          </Button>
        </ComposerPrimitive.Send>
      </ComposerPrimitive.Root>
    </ThreadPrimitive.If>
  );
};

const UserMessage: FC = () => {
  return (
    <MessagePrimitive.Root className='grid w-full max-w-2xl grid-cols-[auto_1fr] gap-3 py-4'>
      <div className='flex size-8 shrink-0 select-none items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium'>
        You
      </div>
      <div className='flex flex-col gap-2 overflow-hidden'>
        <div className='text-sm'>
          <MessagePrimitive.Content />
        </div>
      </div>
    </MessagePrimitive.Root>
  );
};

const AssistantMessage: FC = () => {
  return (
    <MessagePrimitive.Root className='relative grid w-full max-w-2xl grid-cols-[auto_1fr] gap-3 py-4'>
      <div className='flex size-8 shrink-0 select-none items-center justify-center rounded-full bg-muted text-muted-foreground text-xs font-medium'>
        AI
      </div>
      <div className='flex flex-col gap-2 overflow-hidden'>
        <div className='text-sm'>
          <MessagePrimitive.Content />
        </div>
        <AssistantMessageActions />
      </div>
    </MessagePrimitive.Root>
  );
};

const AssistantMessageActions: FC = () => {
  return <div className='flex gap-1'>{/* TODO: 添加消息操作按钮 */}</div>;
};
