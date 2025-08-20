import { LucideIcon } from 'lucide-react';

// 菜单项类型定义
export interface MenuItemType {
  title: string;
  url: string;
  description?: string;
}

// 主导航菜单类型
export interface NavMainItemType {
  title: string;
  url: string;
  icon: LucideIcon;
  isActive?: boolean;
  description?: string;
  items?: MenuItemType[];
}

// 用户信息类型
export interface AdminUserType {
  name: string;
  email: string;
  avatar: string;
  role: string;
}

// 系统信息类型
export interface SystemInfoType {
  name: string;
  version: string;
  description: string;
}

// 快捷统计类型
export interface QuickStatType {
  title: string;
  value: string;
  change: string;
  icon: LucideIcon;
}

// 管理端菜单数据类型
export interface AdminMenuDataType {
  system: SystemInfoType;
  user: AdminUserType;
  navMain: NavMainItemType[];
  quickStats: QuickStatType[];
}
