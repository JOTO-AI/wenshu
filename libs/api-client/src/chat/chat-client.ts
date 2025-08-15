// 智能问数API客户端
import { ApiClient } from '../core/client.js';
import {
  ChatQueryRequest,
  ChatQueryResponse,
  FeedbackRequest,
  ChatHistoryRequest,
  ChatHistoryResponse,
  FileUploadRequest,
  FileUploadResponse,
  ChartDownloadRequest,
  ApiResponse,
} from '@wenshu/shared-types';

/**
 * 智能问数API客户端
 */
export class ChatApiClient {
  constructor(private client: ApiClient) {}

  /**
   * 发送聊天查询
   */
  async query(request: ChatQueryRequest): Promise<ApiResponse<ChatQueryResponse>> {
    return this.client.post<ChatQueryResponse>('/chat/query', request);
  }

  /**
   * 获取聊天历史
   */
  async getHistory(request: ChatHistoryRequest): Promise<ApiResponse<ChatHistoryResponse>> {
    return this.client.get<ChatHistoryResponse>('/chat/history', request);
  }

  /**
   * 获取特定查询结果
   */
  async getQuery(queryId: string): Promise<ApiResponse<ChatQueryResponse>> {
    return this.client.get<ChatQueryResponse>(`/chat/queries/${queryId}`);
  }

  /**
   * 删除查询记录
   */
  async deleteQuery(queryId: string): Promise<ApiResponse<void>> {
    return this.client.delete<void>(`/chat/queries/${queryId}`);
  }

  /**
   * 提交反馈
   */
  async submitFeedback(request: FeedbackRequest): Promise<ApiResponse<void>> {
    return this.client.post<void>('/chat/feedback', request);
  }

  /**
   * 上传文件
   */
  async uploadFile(request: FileUploadRequest): Promise<ApiResponse<FileUploadResponse>> {
    // 注意：实际实现中需要处理FormData
    const formData = new FormData();
    formData.append('file', request.file);
    formData.append('fileName', request.fileName);
    formData.append('fileType', request.fileType);

    return this.client.request<FileUploadResponse>({
      method: 'POST',
      url: '/chat/upload',
      data: formData,
      headers: {
        // 移除Content-Type让浏览器自动设置multipart/form-data
      },
    });
  }

  /**
   * 下载图表
   */
  async downloadChart(request: ChartDownloadRequest): Promise<Blob> {
    // 注意：这里返回Blob而不是ApiResponse
    const response = await fetch(`${this.client['config'].baseURL}/chat/download-chart`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: this.client['token'] ? `Bearer ${this.client['token']}` : '',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Download failed: ${response.statusText}`);
    }

    return response.blob();
  }

  /**
   * 创建新会话
   */
  async createSession(title?: string): Promise<ApiResponse<{ sessionId: string }>> {
    return this.client.post<{ sessionId: string }>('/chat/sessions', { title });
  }

  /**
   * 删除会话
   */
  async deleteSession(sessionId: string): Promise<ApiResponse<void>> {
    return this.client.delete<void>(`/chat/sessions/${sessionId}`);
  }

  /**
   * 重命名会话
   */
  async renameSession(sessionId: string, title: string): Promise<ApiResponse<void>> {
    return this.client.put<void>(`/chat/sessions/${sessionId}`, { title });
  }
}