// 用户管理API类型定义
import { UserRole, Status } from '../common/base.js';
import { PaginationParams, SortParams, FilterParams } from '../common/api.js';

/**
 * 用户创建请求
 */
export interface CreateUserRequest {
  email: string;
  fullName?: string;
  role: UserRole;
  password: string;
  isActive?: boolean;
}

/**
 * 用户更新请求
 */
export interface UpdateUserRequest {
  fullName?: string;
  role?: UserRole;
  isActive?: boolean;
}

/**
 * 用户查询参数
 */
export interface UserQueryParams extends PaginationParams, SortParams, FilterParams {
  role?: UserRole;
  status?: Status;
  isActive?: boolean;
}

/**
 * 用户列表响应
 */
export interface UserListResponse {
  users: UserSummary[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

/**
 * 用户摘要信息
 */
export interface UserSummary {
  id: string;
  email: string;
  fullName?: string;
  role: UserRole;
  isActive: boolean;
  lastLogin?: string;
  createdAt: string;
}

/**
 * 用户详细信息
 */
export interface UserDetail extends UserSummary {
  updatedAt: string;
  loginCount: number;
  permissions: string[];
}

/**
 * 批量用户操作请求
 */
export interface BatchUserOperationRequest {
  userIds: string[];
  operation: 'activate' | 'deactivate' | 'delete';
}

/**
 * 用户统计信息
 */
export interface UserStats {
  totalUsers: number;
  activeUsers: number;
  inactiveUsers: number;
  usersByRole: Record<UserRole, number>;
  recentRegistrations: number;
}