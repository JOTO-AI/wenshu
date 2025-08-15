// 统一API客户端入口
import { ApiClient, ApiClientConfig } from './core/client.js';
import { AuthApiClient } from './auth/auth-client.js';
import { ChatApiClient } from './chat/chat-client.js';
import { UsersApiClient } from './users/users-client.js';

/**
 * 统一API客户端
 * 提供所有功能模块的API访问
 */
export class WenshuApiClient {
  private apiClient: ApiClient;
  
  public readonly auth: AuthApiClient;
  public readonly chat: ChatApiClient;
  public readonly users: UsersApiClient;

  constructor(config: ApiClientConfig) {
    this.apiClient = new ApiClient(config);
    
    // 初始化各功能模块的API客户端
    this.auth = new AuthApiClient(this.apiClient);
    this.chat = new ChatApiClient(this.apiClient);
    this.users = new UsersApiClient(this.apiClient);
  }

  /**
   * 设置认证token
   */
  setToken(token: string) {
    this.apiClient.setToken(token);
  }

  /**
   * 清除认证token
   */
  clearToken() {
    this.apiClient.clearToken();
  }

  /**
   * 获取原始API客户端（用于自定义请求）
   */
  getRawClient(): ApiClient {
    return this.apiClient;
  }
}

/**
 * 创建API客户端实例的工厂函数
 */
export function createApiClient(config: ApiClientConfig): WenshuApiClient {
  return new WenshuApiClient(config);
}

/**
 * 默认配置的API客户端实例
 */
export function createDefaultApiClient(): WenshuApiClient {
  return new WenshuApiClient({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
    timeout: 10000,
    withCredentials: true,
  });
}