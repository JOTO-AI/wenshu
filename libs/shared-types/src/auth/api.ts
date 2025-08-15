// 认证API类型定义
import { UserRole } from '../common/base.js';

/**
 * 登录请求
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * SSO登录请求
 */
export interface SSOLoginRequest {
  ssoToken: string;
  provider?: string;
}

/**
 * 登录响应
 */
export interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
  expiresIn: number;
  user: UserInfo;
}

/**
 * Token刷新请求
 */
export interface RefreshTokenRequest {
  refreshToken: string;
}

/**
 * Token刷新响应
 */
export interface RefreshTokenResponse {
  accessToken: string;
  expiresIn: number;
}

/**
 * 用户信息
 */
export interface UserInfo {
  id: string;
  email: string;
  fullName?: string;
  role: UserRole;
  permissions: string[];
  isActive: boolean;
  lastLogin?: string;
  createdAt: string;
}

/**
 * 密码修改请求
 */
export interface ChangePasswordRequest {
  currentPassword: string;
  newPassword: string;
}

/**
 * 用户资料更新请求
 */
export interface UpdateProfileRequest {
  fullName?: string;
  email?: string;
}