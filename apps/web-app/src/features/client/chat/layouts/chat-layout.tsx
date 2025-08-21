import { ReactNode, useState } from 'react';
import { ThreadList } from '../../../../components/assistant-ui/thread-list';
import { Thread } from '../../../../components/assistant-ui/thread';
import { Button } from '@workspace/ui';
import { MenuIcon, X } from 'lucide-react';

interface ChatLayoutProps {
  children?: ReactNode;
}

export const ChatLayout = ({ children }: ChatLayoutProps) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-dvh bg-background">
      {/* 移动端侧边栏遮罩 */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
      
      {/* 左侧边栏 */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-background border-r transform transition-transform duration-300 ease-in-out
        md:relative md:translate-x-0 md:z-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between p-4 border-b md:hidden">
          <h2 className="text-lg font-semibold">Conversations</h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
        <div className="p-4">
          <ThreadList />
        </div>
      </div>

      {/* 主内容区域 */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* 顶部栏 */}
        <header className="flex items-center justify-between p-4 border-b bg-background">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <MenuIcon className="h-4 w-4" />
            </Button>
            <h1 className="text-lg font-semibold truncate">
              智能问数 - AI数据分析助手
            </h1>
          </div>
          <div className="flex items-center gap-2">
            {/* 可以在这里添加更多操作按钮 */}
          </div>
        </header>

        {/* 聊天区域 */}
        <div className="flex-1 overflow-hidden">
          {children || <Thread className="h-full" />}
        </div>
      </div>
    </div>
  );
};

export default ChatLayout;