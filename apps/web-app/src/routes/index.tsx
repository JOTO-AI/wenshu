// 路由入口文件
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { AuthLayout } from '../layouts';
import { AuthGuard } from './guards';

// 懒加载路由组件
const ClientRoutes = lazy(() => import('./client-routes'));
const AdminRoutes = lazy(() => import('./admin-routes'));

// 懒加载认证页面
const LoginPage = lazy(() => import('../auth/pages'));

// 全局加载组件
const GlobalLoadingSpinner = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
  </div>
);

export const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Suspense fallback={<GlobalLoadingSpinner />}>
        <Routes>
          {/* 认证路由 */}
          <Route 
            path="/login" 
            element={
              <AuthLayout>
                <LoginPage />
              </AuthLayout>
            } 
          />
          
          {/* 管理端路由 - 需要管理员权限 */}
          <Route path="/admin/*" element={<AdminRoutes />} />
          
          {/* 用户端路由 - 需要登录 */}
          <Route 
            path="/*" 
            element={
              <AuthGuard>
                <ClientRoutes />
              </AuthGuard>
            } 
          />
          
          {/* 默认重定向 */}
          <Route path="/" element={<Navigate to="/chat" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
};

export default AppRoutes;