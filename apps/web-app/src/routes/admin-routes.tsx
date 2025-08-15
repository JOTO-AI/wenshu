// 管理端路由配置
import { Routes, Route } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { AdminLayout } from '../layouts';
import { AdminGuard } from './guards/admin-guard';

// 懒加载管理页面组件
const AnalyticsPage = lazy(() => import('../features/admin/analytics/pages'));
const PermissionsPage = lazy(() => import('../features/admin/permissions/pages'));
const DataSourcesPage = lazy(() => import('../features/admin/datasources/pages'));
const KnowledgePage = lazy(() => import('../features/admin/knowledge/pages'));
const DatasetsPage = lazy(() => import('../features/admin/datasets/pages'));
const AuditLogsPage = lazy(() => import('../features/admin/audit-logs/pages'));

// 加载中组件
const LoadingSpinner = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
  </div>
);

export const AdminRoutes = () => {
  return (
    <AdminGuard>
      <AdminLayout>
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            <Route path="/admin" element={<AnalyticsPage />} />
            <Route path="/admin/analytics" element={<AnalyticsPage />} />
            <Route path="/admin/permissions" element={<PermissionsPage />} />
            <Route path="/admin/datasources" element={<DataSourcesPage />} />
            <Route path="/admin/knowledge" element={<KnowledgePage />} />
            <Route path="/admin/datasets" element={<DatasetsPage />} />
            <Route path="/admin/audit-logs" element={<AuditLogsPage />} />
          </Routes>
        </Suspense>
      </AdminLayout>
    </AdminGuard>
  );
};

export default AdminRoutes;