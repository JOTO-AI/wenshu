import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  Separator,
} from '@wenshu/ui';
import { Monitor, Palette, Shield } from 'lucide-react';
import React from 'react';
import { LayoutSwitcher } from '../../../../layouts/admin-layout/components';

const SettingsPage: React.FC = () => {
  return (
    <div className='space-y-6'>
      {/* 页面头部 */}
      <div className='space-y-2'>
        <h1 className='text-3xl font-bold tracking-tight flex items-center gap-2'>
          <Monitor className='h-8 w-8' />
          系统设置
        </h1>
        <p className='text-muted-foreground'>
          管理系统的全局设置、界面布局和配置选项
        </p>
      </div>

      <Separator />

      <div className='grid gap-6'>
        {/* 界面设置 */}
        <section>
          <div className='mb-4'>
            <h2 className='text-xl font-semibold flex items-center gap-2'>
              <Palette className='h-5 w-5' />
              界面设置
            </h2>
            <p className='text-sm text-muted-foreground'>
              自定义您的工作界面，选择最适合的布局模式
            </p>
          </div>

          <LayoutSwitcher />
        </section>

        <Separator />

        {/* 通用设置 */}
        <section>
          <div className='mb-4'>
            <h2 className='text-xl font-semibold'>通用设置</h2>
            <p className='text-sm text-muted-foreground'>
              系统的基本配置和首选项
            </p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className='text-base'>系统偏好</CardTitle>
              <CardDescription>配置系统的基本行为和默认设置</CardDescription>
            </CardHeader>
            <CardContent>
              <div className='space-y-4'>
                <div className='flex items-center justify-between'>
                  <div>
                    <div className='font-medium'>自动保存用户偏好</div>
                    <div className='text-sm text-muted-foreground'>
                      自动保存布局设置和用户操作习惯
                    </div>
                  </div>
                  <div className='text-green-600 text-sm font-medium'>
                    已启用
                  </div>
                </div>
                <Separator />
                <div className='text-sm text-muted-foreground'>
                  更多设置选项将在后续版本中添加...
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        <Separator />

        {/* 安全设置 */}
        <section>
          <div className='mb-4'>
            <h2 className='text-xl font-semibold flex items-center gap-2'>
              <Shield className='h-5 w-5' />
              安全设置
            </h2>
            <p className='text-sm text-muted-foreground'>
              管理用户权限、会话设置和安全策略
            </p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className='text-base'>安全策略</CardTitle>
              <CardDescription>
                配置系统安全相关的设置和权限控制
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className='space-y-4'>
                <div className='flex items-center justify-between'>
                  <div>
                    <div className='font-medium'>会话自动过期</div>
                    <div className='text-sm text-muted-foreground'>
                      无操作30分钟后自动退出登录
                    </div>
                  </div>
                  <div className='text-green-600 text-sm font-medium'>
                    已启用
                  </div>
                </div>
                <Separator />
                <div className='text-sm text-muted-foreground'>
                  安全设置功能开发中...
                </div>
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </div>
  );
};

export default SettingsPage;
