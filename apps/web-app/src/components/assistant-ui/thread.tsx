import {
  ComposerPrimitive,
  MessagePrimitive,
  ThreadPrimitive,
} from '@assistant-ui/react';
import { Button, cn } from '@workspace/ui';
import type { FC } from 'react';

interface ThreadProps {
  className?: string;
  welcome?: {
    suggestions?: Array<{ prompt: string }>;
  };
}

export const Thread: FC<ThreadProps> = ({ className, welcome }) => {
  return (
    <ThreadPrimitive.Root
      className={cn('aui-root aui-thread-root flex flex-col h-full', className)}
    >
      <ThreadPrimitive.Viewport className='flex-1 overflow-y-auto px-4 py-4'>
        <div className='max-w-4xl mx-auto'>
          <ThreadWelcome welcome={welcome} />
          <ThreadMessages />
          <ThreadScrollToBottom />
        </div>
      </ThreadPrimitive.Viewport>
      <div className='border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60'>
        <div className='max-w-4xl mx-auto p-4'>
          <ThreadComposer />
        </div>
      </div>
    </ThreadPrimitive.Root>
  );
};

const ThreadWelcome: FC<{ welcome?: ThreadProps['welcome'] }> = ({
  welcome,
}) => {
  return (
    <ThreadPrimitive.Empty>
      <div className='flex flex-col items-center justify-center min-h-[60vh] space-y-8 text-center py-12'>
        <div className='space-y-4'>
          <div className='w-16 h-16 mx-auto bg-primary/10 rounded-full flex items-center justify-center'>
            <svg
              className='w-8 h-8 text-primary'
              fill='none'
              stroke='currentColor'
              viewBox='0 0 24 24'
            >
              <path
                strokeLinecap='round'
                strokeLinejoin='round'
                strokeWidth={2}
                d='M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'
              />
            </svg>
          </div>
          <h2 className='text-3xl font-bold'>智能问数助手</h2>
          <p className='text-muted-foreground text-lg max-w-md'>
            开始对话，我可以帮助您分析数据、生成图表和回答问题
          </p>
        </div>

        {welcome?.suggestions && (
          <div className='w-full max-w-3xl space-y-3'>
            <p className='text-sm text-muted-foreground font-medium'>
              试试这些常用功能：
            </p>
            <div className='grid grid-cols-1 md:grid-cols-2 gap-3'>
              {welcome.suggestions.map((suggestion, index) => (
                <ThreadPrimitive.Suggestion
                  key={index}
                  prompt={suggestion.prompt}
                  method='replace'
                  asChild
                >
                  <Button
                    variant='outline'
                    className='h-auto p-4 whitespace-normal text-left justify-start hover:bg-accent/50 transition-colors'
                  >
                    <span className='text-sm'>{suggestion.prompt}</span>
                  </Button>
                </ThreadPrimitive.Suggestion>
              ))}
            </div>
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
        className='aui-thread-scroll-to-bottom fixed bottom-24 right-8 rounded-full shadow-lg bg-background border'
      >
        <svg
          className='w-4 h-4'
          fill='none'
          stroke='currentColor'
          viewBox='0 0 24 24'
        >
          <path
            strokeLinecap='round'
            strokeLinejoin='round'
            strokeWidth={2}
            d='M19 14l-7 7m0 0l-7-7m7 7V3'
          />
        </svg>
      </Button>
    </ThreadPrimitive.ScrollToBottom>
  );
};

const ThreadComposer: FC = () => {
  return (
    <ThreadPrimitive.If running={false}>
      <ComposerPrimitive.Root className='flex w-full items-end gap-3 rounded-xl border bg-background shadow-sm p-3'>
        <ComposerPrimitive.Input
          autoFocus
          placeholder='输入您的问题...'
          className='flex-1 resize-none border-0 bg-transparent px-0 py-2 text-base outline-none placeholder:text-muted-foreground min-h-[24px] max-h-32'
        />
        <ComposerPrimitive.Send asChild>
          <Button
            size='icon'
            className='size-9 rounded-lg shrink-0 flex items-center justify-center'
          >
            <svg
              className='w-4 h-4 rotate-90'
              fill='none'
              stroke='white'
              viewBox='0 0 24 24'
            >
              <path
                strokeLinecap='round'
                strokeLinejoin='round'
                strokeWidth={2}
                d='M12 19l9 2-9-18-9 18 9-2zm0 0v-8'
              />
            </svg>
          </Button>
        </ComposerPrimitive.Send>
      </ComposerPrimitive.Root>
    </ThreadPrimitive.If>
  );
};

const UserMessage: FC = () => {
  return (
    <MessagePrimitive.Root className='flex w-full justify-end py-2'>
      <div className='flex flex-col gap-2 max-w-[70%]'>
        <div className='bg-primary text-primary-foreground rounded-2xl rounded-br-md px-4 py-3'>
          <MessagePrimitive.Content />
        </div>
      </div>
    </MessagePrimitive.Root>
  );
};

const AssistantMessage: FC = () => {
  return (
    <MessagePrimitive.Root className='flex w-full justify-start py-2'>
      <div className='flex gap-3 max-w-[85%]'>
        <div className='flex size-8 shrink-0 select-none items-center justify-center rounded-full bg-muted text-muted-foreground text-xs font-medium'>
          AI
        </div>
        <div className='flex flex-col gap-2 overflow-hidden'>
          <div className='bg-muted rounded-2xl rounded-bl-md px-4 py-3'>
            <MessagePrimitive.Content />
          </div>
          <AssistantMessageActions />
        </div>
      </div>
    </MessagePrimitive.Root>
  );
};

const AssistantMessageActions: FC = () => {
  return <div className='flex gap-1'>{/* TODO: 添加消息操作按钮 */}</div>;
};
