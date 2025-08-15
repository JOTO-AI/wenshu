// 认证守卫
import { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';

interface AuthGuardProps {
  children: ReactNode;
}

export const AuthGuard = ({ children }: AuthGuardProps) => {
  // TODO: 从认证store获取用户信息
  // const { isAuthenticated } = useAuthStore();
  
  // 临时模拟认证状态
  const isAuthenticated = true; // TODO: 替换为真实的认证状态
  
  // 如果未登录，重定向到登录页面
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

export default AuthGuard;