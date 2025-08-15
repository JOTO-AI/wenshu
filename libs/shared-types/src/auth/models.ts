// 认证相关模型类型
import { BaseEntity } from '../common/base.js';
import { UserRole } from '../common/base.js';

/**
 * 用户模型
 */
export interface User extends BaseEntity {
  email: string;
  fullName?: string;
  role: UserRole;
  isActive: boolean;
  lastLogin?: string;
  passwordHash?: string; // 仅后端使用
}

/**
 * 用户会话模型
 */
export interface UserSession extends BaseEntity {
  userId: string;
  tokenJti: string;
  refreshToken: string;
  expiresAt: string;
  ipAddress?: string;
  userAgent?: string;
}

/**
 * 权限模型
 */
export interface Permission extends BaseEntity {
  name: string;
  description?: string;
  resource: string;
  action: string;
}

/**
 * 角色权限关联
 */
export interface RolePermission extends BaseEntity {
  role: UserRole;
  permissionId: string;
}

/**
 * JWT Token载荷
 */
export interface JWTPayload {
  sub: string; // 用户ID
  email: string;
  role: UserRole;
  permissions: string[];
  iat: number;
  exp: number;
  jti: string;
}