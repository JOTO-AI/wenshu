// 用户管理模型类型
import { BaseEntity, Status, ActionType } from '../common/base.js';
import { UserRole } from '../common/base.js';

/**
 * 用户活动日志模型
 */
export interface UserActivityLog extends BaseEntity {
  userId: string;
  action: ActionType;
  resource: string;
  details?: Record<string, any>;
  ipAddress?: string;
  userAgent?: string;
}

/**
 * 用户偏好设置模型
 */
export interface UserPreferences extends BaseEntity {
  userId: string;
  theme: 'light' | 'dark' | 'auto';
  language: string;
  timezone: string;
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
  dashboard: {
    layout: string;
    widgets: string[];
  };
}

/**
 * 用户邀请模型
 */
export interface UserInvitation extends BaseEntity {
  email: string;
  role: UserRole;
  invitedBy: string;
  token: string;
  expiresAt: string;
  status: Status;
  acceptedAt?: string;
}

/**
 * 用户组模型
 */
export interface UserGroup extends BaseEntity {
  name: string;
  description?: string;
  permissions: string[];
  memberCount: number;
  isActive: boolean;
}

/**
 * 用户组成员关联
 */
export interface UserGroupMember extends BaseEntity {
  userId: string;
  groupId: string;
  joinedAt: string;
  role: 'member' | 'admin';
}