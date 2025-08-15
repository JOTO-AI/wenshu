// 管理端布局组件
// 用于管理员界面的布局，注重功能性和信息密度

import { ReactNode } from 'react';

interface AdminLayoutProps {
  children: ReactNode;
}

export const AdminLayout = ({ children }: AdminLayoutProps) => {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* TODO: 添加管理端布局结构 */}
      <header className="bg-white shadow-sm border-b">
        {/* 管理端导航栏 */}
      </header>
      
      <div className="flex">
        <aside className="w-64 bg-white shadow-sm">
          {/* 管理端侧边栏 */}
        </aside>
        
        <main className="flex-1 p-6">
          {/* 面包屑导航 */}
          <nav className="mb-4">
            {/* TODO: 添加面包屑导航 */}
          </nav>
          
          {children}
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;