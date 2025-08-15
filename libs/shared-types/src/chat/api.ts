// 智能问数API类型定义
import { ChartType } from '../common/base.js';

/**
 * 聊天查询请求
 */
export interface ChatQueryRequest {
  query: string;
  sessionId?: string;
  dataSourceIds?: string[];
  context?: Record<string, any>;
}

/**
 * 图表配置
 */
export interface ChartConfig {
  type: ChartType;
  title?: string;
  data: Record<string, any>;
  options: Record<string, any>;
  width?: number;
  height?: number;
}

/**
 * 聊天查询响应
 */
export interface ChatQueryResponse {
  id: string;
  query: string;
  sql?: string;
  data: Record<string, any>[];
  chart?: ChartConfig;
  explanation: string;
  suggestions?: string[];
  sessionId: string;
  executionTime: number;
  createdAt: string;
}

/**
 * 反馈请求
 */
export interface FeedbackRequest {
  queryId: string;
  feedbackType: 'like' | 'dislike';
  comment?: string;
}

/**
 * 会话历史请求
 */
export interface ChatHistoryRequest {
  sessionId?: string;
  limit?: number;
  offset?: number;
}

/**
 * 会话历史响应
 */
export interface ChatHistoryResponse {
  sessions: any[]; // 使用any避免循环依赖，实际使用时会从models导入ChatSession
  total: number;
}

/**
 * 文件上传请求
 */
export interface FileUploadRequest {
  file: File;
  fileName: string;
  fileType: string;
}

/**
 * 文件上传响应
 */
export interface FileUploadResponse {
  fileId: string;
  fileName: string;
  fileUrl: string;
  previewData?: Record<string, any>[];
}

/**
 * 图表下载请求
 */
export interface ChartDownloadRequest {
  queryId: string;
  format: 'png' | 'jpg' | 'pdf' | 'svg';
  width?: number;
  height?: number;
}

// ChatSession类型在models.ts中定义，这里只需要引用