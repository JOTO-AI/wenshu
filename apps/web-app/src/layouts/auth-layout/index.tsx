// 认证页面布局组件
// 用于登录、注册等认证页面的布局

import { ReactNode } from 'react';

interface AuthLayoutProps {
  children: ReactNode;
}

export const AuthLayout = ({ children }: AuthLayoutProps) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="max-w-md w-full space-y-8 p-8">
        {/* TODO: 添加认证页面布局结构 */}
        <div className="text-center">
          {/* Logo */}
          <h1 className="text-3xl font-bold text-gray-900">智能问数</h1>
          <p className="mt-2 text-gray-600">企业级私有化对话式数据分析平台</p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          {children}
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;