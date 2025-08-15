// 智能问数模型类型
import { BaseEntity, DataSourceType } from '../common/base.js';
import { ChartConfig } from './api.js';

/**
 * 聊天会话模型
 */
export interface ChatSession extends BaseEntity {
  title?: string;
  userId: string;
  isActive: boolean;
}

/**
 * 聊天查询模型
 */
export interface ChatQuery extends BaseEntity {
  sessionId: string;
  userId: string;
  query: string;
  sql?: string;
  data: Record<string, any>[];
  chart?: ChartConfig;
  explanation: string;
  suggestions?: string[];
  executionTime: number;
  dataSourceIds: string[];
}

/**
 * 数据源模型
 */
export interface DataSource extends BaseEntity {
  name: string;
  type: DataSourceType;
  connectionString: string;
  isActive: boolean;
  userId: string;
  description?: string;
  config: Record<string, any>;
}

/**
 * 查询反馈模型
 */
export interface QueryFeedback extends BaseEntity {
  queryId: string;
  userId: string;
  feedbackType: 'like' | 'dislike';
  comment?: string;
}

/**
 * 文件上传模型
 */
export interface UploadedFile extends BaseEntity {
  fileName: string;
  originalName: string;
  fileType: string;
  fileSize: number;
  fileUrl: string;
  userId: string;
  isProcessed: boolean;
  metadata?: Record<string, any>;
}