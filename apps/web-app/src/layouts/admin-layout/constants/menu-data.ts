import {
  BarChart3,
  Database,
  FileText,
  Home,
  Key,
  Layers,
  Menu,
  Settings,
  Shield,
  Users,
} from 'lucide-react';

// 智能问数系统 - 管理端菜单数据
export const adminMenuData = {
  system: {
    name: '智能问数',
    version: 'v1.0.0',
    description: '智能问数系统管理端',
  },

  // 管理员用户信息（示例）
  user: {
    name: '系统管理员',
    email: 'admin@wenshu.com',
    avatar: '/avatars/admin.jpg',
    role: 'Super Admin',
  },

  // 主导航菜单
  navMain: [
    {
      title: '仪表板',
      url: '/admin/dashboard',
      icon: Home,
      isActive: true,
      description: '系统概览和关键指标',
    },
    {
      title: '数据源管理',
      url: '/admin/datasources',
      icon: Database,
      description: '管理数据连接和数据源配置',
      items: [
        {
          title: '数据库连接',
          url: '/admin/datasources/database',
        },
        {
          title: '文件数据源',
          url: '/admin/datasources/files',
        },
        {
          title: 'API接口',
          url: '/admin/datasources/api',
        },
      ],
    },
    {
      title: '应用管理',
      url: '/admin/applications',
      icon: Layers,
      description: '管理应用配置和部署',
      items: [
        {
          title: '应用列表',
          url: '/admin/applications/list',
        },
        {
          title: '应用配置',
          url: '/admin/applications/config',
        },
        {
          title: '版本管理',
          url: '/admin/applications/versions',
        },
      ],
    },
    {
      title: '用户管理',
      url: '/admin/users',
      icon: Users,
      description: '管理系统用户和用户组',
      items: [
        {
          title: '用户列表',
          url: '/admin/users/list',
        },
        {
          title: '用户组',
          url: '/admin/users/groups',
        },
        {
          title: '用户导入',
          url: '/admin/users/import',
        },
      ],
    },
    {
      title: '角色管理',
      url: '/admin/roles',
      icon: Shield,
      description: '管理用户角色和权限分配',
      items: [
        {
          title: '角色列表',
          url: '/admin/roles/list',
        },
        {
          title: '权限分配',
          url: '/admin/roles/permissions',
        },
        {
          title: '角色模板',
          url: '/admin/roles/templates',
        },
      ],
    },
    {
      title: '权限管理',
      url: '/admin/permissions',
      icon: Key,
      description: '管理系统权限和访问控制',
      items: [
        {
          title: '权限列表',
          url: '/admin/permissions/list',
        },
        {
          title: '资源权限',
          url: '/admin/permissions/resources',
        },
        {
          title: 'API权限',
          url: '/admin/permissions/api',
        },
      ],
    },
    {
      title: '日志管理',
      url: '/admin/logs',
      icon: FileText,
      description: '查看系统日志和审计记录',
      items: [
        {
          title: '操作日志',
          url: '/admin/logs/operations',
        },
        {
          title: '系统日志',
          url: '/admin/logs/system',
        },
        {
          title: '错误日志',
          url: '/admin/logs/errors',
        },
      ],
    },
    {
      title: '菜单管理',
      url: '/admin/menus',
      icon: Menu,
      description: '管理系统菜单和导航结构',
      items: [
        {
          title: '菜单结构',
          url: '/admin/menus/structure',
        },
        {
          title: '菜单权限',
          url: '/admin/menus/permissions',
        },
        {
          title: '菜单配置',
          url: '/admin/menus/config',
        },
      ],
    },
    {
      title: '系统设置',
      url: '/admin/settings',
      icon: Settings,
      description: '系统配置和参数设置',
      items: [
        {
          title: '基础设置',
          url: '/admin/settings/basic',
        },
        {
          title: '安全设置',
          url: '/admin/settings/security',
        },
        {
          title: '邮件设置',
          url: '/admin/settings/email',
        },
        {
          title: '系统参数',
          url: '/admin/settings/parameters',
        },
      ],
    },
  ],

  // 快捷统计（仪表板卡片）
  quickStats: [
    {
      title: '今日查询',
      value: '1,234',
      change: '+12%',
      icon: BarChart3,
    },
    {
      title: '活跃用户',
      value: '89',
      change: '+5%',
      icon: Users,
    },
    {
      title: '数据源',
      value: '15',
      change: '0%',
      icon: Database,
    },
    {
      title: '系统健康度',
      value: '98%',
      change: '+1%',
      icon: Shield,
    },
  ],
};

export default adminMenuData;
