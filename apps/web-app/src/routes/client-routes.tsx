// 用户端路由配置
import { lazy, Suspense } from 'react';
import { Route, Routes } from 'react-router-dom';
import { ClientLayout } from '../layouts';

// 懒加载页面组件
const ChatPage = lazy(() => import('../features/client/chat/pages'));
const DashboardPage = lazy(() => import('../features/client/dashboard/pages'));
const ProfilePage = lazy(() => import('../features/client/profile/pages'));
const TestUIPage = lazy(() => import('../pages/test-ui'));

// 加载中组件
const LoadingSpinner = () => (
  <div className='flex items-center justify-center min-h-screen'>
    <div className='animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500'></div>
  </div>
);

export const ClientRoutes = () => {
  return (
    <ClientLayout>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path='/chat' element={<ChatPage />} />
          <Route path='/dashboard' element={<DashboardPage />} />
          <Route path='/profile' element={<ProfilePage />} />
          <Route path='/test-ui' element={<TestUIPage />} />
          {/* 默认重定向到聊天页面 */}
          <Route path='/' element={<ChatPage />} />
        </Routes>
      </Suspense>
    </ClientLayout>
  );
};

export default ClientRoutes;
