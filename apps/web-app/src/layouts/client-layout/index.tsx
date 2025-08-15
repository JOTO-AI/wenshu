// 用户端布局组件
// 用于普通用户界面的布局，注重美观和用户体验

import { ReactNode } from 'react';

interface ClientLayoutProps {
  children: ReactNode;
}

export const ClientLayout = ({ children }: ClientLayoutProps) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* TODO: 添加用户端布局结构 */}
      <header className="bg-white shadow-sm">
        {/* 用户端导航栏 */}
      </header>
      
      <main className="container mx-auto px-4 py-6">
        {children}
      </main>
      
      <footer className="bg-white border-t">
        {/* 用户端页脚 */}
      </footer>
    </div>
  );
};

export default ClientLayout;