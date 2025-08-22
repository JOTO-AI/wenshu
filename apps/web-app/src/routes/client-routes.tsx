// 用户端路由配置
import { lazy, Suspense } from 'react';
import { Route, Routes } from 'react-router-dom';
import { ClientLayout } from '../layouts';

// 懒加载页面组件
const ChatPage = lazy(() => import('../features/client/chat/pages'));
const DashboardPage = lazy(() => import('../features/client/dashboard/pages'));
const ProfilePage = lazy(() => import('../features/client/profile/pages'));
const TestUIPage = lazy(() => import('../features/client/dev/pages/test-ui'));

// 加载中组件
const LoadingSpinner = () => (
  <div className='flex items-center justify-center min-h-screen'>
    <div className='animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500'></div>
  </div>
);

export const ClientRoutes = () => {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        {/* 聊天页面使用自己的布局 */}
        <Route path='/chat' element={<ChatPage />} />
        <Route path='/' element={<ChatPage />} />
        
        {/* 其他页面使用通用客户端布局 */}
        <Route path='/dashboard' element={
          <ClientLayout>
            <DashboardPage />
          </ClientLayout>
        } />
        <Route path='/profile' element={
          <ClientLayout>
            <ProfilePage />
          </ClientLayout>
        } />
        <Route path='/test-ui' element={
          <ClientLayout>
            <TestUIPage />
          </ClientLayout>
        } />
      </Routes>
    </Suspense>
  );
};

export default ClientRoutes;
