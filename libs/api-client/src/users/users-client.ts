// 用户管理API客户端
import { ApiClient } from '../core/client.js';
import {
  CreateUserRequest,
  UpdateUserRequest,
  UserQueryParams,
  UserListResponse,
  UserDetail,
  BatchUserOperationRequest,
  UserStats,
  ApiResponse,
} from '@wenshu/shared-types';

/**
 * 用户管理API客户端
 */
export class UsersApiClient {
  constructor(private client: ApiClient) {}

  /**
   * 获取用户列表
   */
  async getUsers(params?: UserQueryParams): Promise<ApiResponse<UserListResponse>> {
    return this.client.get<UserListResponse>('/users', params);
  }

  /**
   * 获取用户详情
   */
  async getUser(userId: string): Promise<ApiResponse<UserDetail>> {
    return this.client.get<UserDetail>(`/users/${userId}`);
  }

  /**
   * 创建用户
   */
  async createUser(request: CreateUserRequest): Promise<ApiResponse<UserDetail>> {
    return this.client.post<UserDetail>('/users', request);
  }

  /**
   * 更新用户
   */
  async updateUser(userId: string, request: UpdateUserRequest): Promise<ApiResponse<UserDetail>> {
    return this.client.put<UserDetail>(`/users/${userId}`, request);
  }

  /**
   * 删除用户
   */
  async deleteUser(userId: string): Promise<ApiResponse<void>> {
    return this.client.delete<void>(`/users/${userId}`);
  }

  /**
   * 激活用户
   */
  async activateUser(userId: string): Promise<ApiResponse<void>> {
    return this.client.post<void>(`/users/${userId}/activate`);
  }

  /**
   * 停用用户
   */
  async deactivateUser(userId: string): Promise<ApiResponse<void>> {
    return this.client.post<void>(`/users/${userId}/deactivate`);
  }

  /**
   * 批量操作用户
   */
  async batchOperation(request: BatchUserOperationRequest): Promise<ApiResponse<void>> {
    return this.client.post<void>('/users/batch', request);
  }

  /**
   * 获取用户统计信息
   */
  async getUserStats(): Promise<ApiResponse<UserStats>> {
    return this.client.get<UserStats>('/users/stats');
  }

  /**
   * 重置用户密码
   */
  async resetPassword(userId: string): Promise<ApiResponse<{ temporaryPassword: string }>> {
    return this.client.post<{ temporaryPassword: string }>(`/users/${userId}/reset-password`);
  }

  /**
   * 发送用户邀请
   */
  async inviteUser(email: string, role: string): Promise<ApiResponse<void>> {
    return this.client.post<void>('/users/invite', { email, role });
  }
}