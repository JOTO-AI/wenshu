// 管理端路由配置
import { Suspense, lazy } from 'react';
import { Route, Routes } from 'react-router-dom';
import { AdminLayout } from '../layouts';
import { AdminGuard } from './guards/admin-guard';

// 懒加载管理页面组件
const AnalyticsPage = lazy(() => import('../features/admin/analytics/pages'));
const PermissionsPage = lazy(
  () => import('../features/admin/permissions/pages')
);
const DataSourcesPage = lazy(
  () => import('../features/admin/datasources/pages')
);
const KnowledgePage = lazy(() => import('../features/admin/knowledge/pages'));
const DatasetsPage = lazy(() => import('../features/admin/datasets/pages'));
const AuditLogsPage = lazy(() => import('../features/admin/audit-logs/pages'));
const DashboardPage = lazy(() => import('../features/admin/dashboard/pages'));

// 加载中组件
const LoadingSpinner = () => (
  <div className='flex items-center justify-center min-h-screen'>
    <div className='animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500'></div>
  </div>
);

export const AdminRoutes = () => {
  return (
    <AdminGuard>
      <AdminLayout>
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            <Route path='/' element={<AnalyticsPage />} />
            <Route path='/dashboard' element={<DashboardPage />} />
            <Route path='/analytics' element={<AnalyticsPage />} />
            <Route path='/permissions' element={<PermissionsPage />} />
            <Route path='/datasources' element={<DataSourcesPage />} />
            <Route path='/knowledge' element={<KnowledgePage />} />
            <Route path='/datasets' element={<DatasetsPage />} />
            <Route path='/audit-logs' element={<AuditLogsPage />} />
          </Routes>
        </Suspense>
      </AdminLayout>
    </AdminGuard>
  );
};

export default AdminRoutes;
