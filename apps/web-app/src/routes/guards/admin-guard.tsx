// 管理员权限守卫
import { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';

interface AdminGuardProps {
  children: ReactNode;
}

export const AdminGuard = ({ children }: AdminGuardProps) => {
  // TODO: 从认证store获取用户信息
  // const { user, isAuthenticated } = useAuthStore();
  
  // 临时模拟用户权限检查
  const isAuthenticated = true; // TODO: 替换为真实的认证状态
  const userRole = 'ADMIN'; // TODO: 替换为真实的用户角色
  
  // 检查用户是否已登录
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  // 检查用户是否有管理员权限
  if (!['ADMIN', 'SUPERADMIN'].includes(userRole)) {
    return <Navigate to="/chat" replace />;
  }
  
  return <>{children}</>;
};

export default AdminGuard;