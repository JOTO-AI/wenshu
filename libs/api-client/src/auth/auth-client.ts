// 认证API客户端
import { ApiClient } from '../core/client.js';
import {
  LoginRequest,
  LoginResponse,
  SSOLoginRequest,
  RefreshTokenRequest,
  RefreshTokenResponse,
  UserInfo,
  ChangePasswordRequest,
  UpdateProfileRequest,
  ApiResponse,
} from '@wenshu/shared-types';

/**
 * 认证API客户端
 */
export class AuthApiClient {
  constructor(private client: ApiClient) {}

  /**
   * 用户登录
   */
  async login(request: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    return this.client.post<LoginResponse>('/auth/login', request);
  }

  /**
   * SSO登录
   */
  async ssoLogin(request: SSOLoginRequest): Promise<ApiResponse<LoginResponse>> {
    return this.client.post<LoginResponse>('/auth/sso-login', request);
  }

  /**
   * 刷新Token
   */
  async refreshToken(request: RefreshTokenRequest): Promise<ApiResponse<RefreshTokenResponse>> {
    return this.client.post<RefreshTokenResponse>('/auth/refresh', request);
  }

  /**
   * 用户登出
   */
  async logout(): Promise<ApiResponse<void>> {
    return this.client.post<void>('/auth/logout');
  }

  /**
   * 获取当前用户信息
   */
  async getCurrentUser(): Promise<ApiResponse<UserInfo>> {
    return this.client.get<UserInfo>('/auth/me');
  }

  /**
   * 修改密码
   */
  async changePassword(request: ChangePasswordRequest): Promise<ApiResponse<void>> {
    return this.client.post<void>('/auth/change-password', request);
  }

  /**
   * 更新用户资料
   */
  async updateProfile(request: UpdateProfileRequest): Promise<ApiResponse<UserInfo>> {
    return this.client.put<UserInfo>('/auth/profile', request);
  }

  /**
   * 验证Token有效性
   */
  async validateToken(): Promise<ApiResponse<{ valid: boolean }>> {
    return this.client.get<{ valid: boolean }>('/auth/validate');
  }
}