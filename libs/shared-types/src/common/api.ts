// 通用API类型定义
// 用于定义所有API接口的通用类型

/**
 * 通用API响应结构
 */
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  code?: number;
}

/**
 * 分页请求参数
 */
export interface PaginationParams {
  page?: number;
  limit?: number;
  skip?: number;
}

/**
 * 分页响应结构
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

/**
 * 排序参数
 */
export interface SortParams {
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

/**
 * 筛选参数基础接口
 */
export interface FilterParams {
  search?: string;
  startDate?: string;
  endDate?: string;
}

/**
 * HTTP方法类型
 */
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

/**
 * API错误类型
 */
export interface ApiError {
  code: number;
  message: string;
  details?: Record<string, any>;
}