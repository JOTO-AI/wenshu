// 基础类型定义
// 用于定义项目中的基础类型和枚举

/**
 * 用户角色枚举
 */
export enum UserRole {
  CLIENT = 'CLIENT',
  ADMIN = 'ADMIN',
  SUPERADMIN = 'SUPERADMIN'
}

/**
 * 数据源类型枚举
 */
export enum DataSourceType {
  MYSQL = 'mysql',
  POSTGRESQL = 'postgresql',
  ORACLE = 'oracle',
  SQLITE = 'sqlite',
  CSV = 'csv',
  EXCEL = 'excel'
}

/**
 * 图表类型枚举
 */
export enum ChartType {
  LINE = 'line',
  BAR = 'bar',
  PIE = 'pie',
  SCATTER = 'scatter',
  TABLE = 'table'
}

/**
 * 基础实体接口
 */
export interface BaseEntity {
  id: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * 可选的基础实体（用于创建时）
 */
export interface BaseEntityCreate {
  id?: string;
  createdAt?: string;
  updatedAt?: string;
}

/**
 * 状态枚举
 */
export enum Status {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  PENDING = 'pending',
  DELETED = 'deleted'
}

/**
 * 操作类型枚举
 */
export enum ActionType {
  CREATE = 'create',
  READ = 'read',
  UPDATE = 'update',
  DELETE = 'delete'
}

/**
 * 日志级别枚举
 */
export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error'
}