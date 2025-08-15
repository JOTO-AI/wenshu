// 核心API客户端
import { ApiResponse, ApiError, HttpMethod } from '@wenshu/shared-types';

/**
 * API客户端配置
 */
export interface ApiClientConfig {
  baseURL: string;
  timeout?: number;
  headers?: Record<string, string>;
  withCredentials?: boolean;
}

/**
 * 请求配置
 */
export interface RequestConfig {
  method: HttpMethod;
  url: string;
  data?: any;
  params?: Record<string, any>;
  headers?: Record<string, string>;
}

/**
 * 核心API客户端类
 */
export class ApiClient {
  private config: ApiClientConfig;
  private token?: string;

  constructor(config: ApiClientConfig) {
    this.config = config;
  }

  /**
   * 设置认证token
   */
  setToken(token: string) {
    this.token = token;
  }

  /**
   * 清除认证token
   */
  clearToken() {
    this.token = undefined;
  }

  /**
   * 发送HTTP请求
   */
  async request<T = any>(config: RequestConfig): Promise<ApiResponse<T>> {
    const url = `${this.config.baseURL}${config.url}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...this.config.headers,
      ...config.headers,
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        method: config.method,
        headers,
        body: config.data ? JSON.stringify(config.data) : undefined,
        credentials: this.config.withCredentials ? 'include' : 'same-origin',
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error((data as any)?.message || `HTTP ${response.status}`);
      }

      return data as ApiResponse<T>;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * GET请求
   */
  async get<T = any>(url: string, params?: Record<string, any>): Promise<ApiResponse<T>> {
    const queryString = params ? new URLSearchParams(params).toString() : '';
    const fullUrl = queryString ? `${url}?${queryString}` : url;
    
    return this.request<T>({
      method: 'GET',
      url: fullUrl,
    });
  }

  /**
   * POST请求
   */
  async post<T = any>(url: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>({
      method: 'POST',
      url,
      data,
    });
  }

  /**
   * PUT请求
   */
  async put<T = any>(url: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>({
      method: 'PUT',
      url,
      data,
    });
  }

  /**
   * DELETE请求
   */
  async delete<T = any>(url: string): Promise<ApiResponse<T>> {
    return this.request<T>({
      method: 'DELETE',
      url,
    });
  }

  /**
   * 错误处理
   */
  private handleError(error: any): ApiError {
    if (error instanceof Error) {
      return {
        code: 0,
        message: error.message,
        details: { originalError: error },
      };
    }
    
    return {
      code: 0,
      message: 'Unknown error occurred',
      details: { error },
    };
  }
}