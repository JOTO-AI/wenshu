import * as React from 'react';
import { LoginForm } from '../components/login-form';

export function LoginPage() {
  const [loading, setLoading] = React.useState(false);

  const handleLogin = async (data: { email: string; password: string }) => {
    setLoading(true);
    try {
      // TODO: 实际的登录逻辑
      console.log('Login with email:', data.email);
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 1000));
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSSOLogin = async (provider: string) => {
    setLoading(true);
    try {
      // TODO: 实际的SSO登录逻辑
      console.log('SSO login with:', provider);
      // 模拟SSO重定向
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error('SSO login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4'>
      <div className='w-full max-w-md space-y-8'>
        {/* 品牌Logo区域 */}
        <div className='text-center'>
          <h2 className='text-3xl font-bold text-gray-900 dark:text-white'>
            Wenshu
          </h2>
          <p className='mt-2 text-sm text-gray-600 dark:text-gray-400'>
            智能问数系统
          </p>
        </div>

        {/* 登录表单 */}
        <div className='bg-white dark:bg-gray-800 py-8 px-6 shadow-lg rounded-lg'>
          <LoginForm
            onSubmit={handleLogin}
            onSSOLogin={handleSSOLogin}
            loading={loading}
          />
        </div>

        {/* 帮助链接 */}
        <div className='text-center text-sm text-gray-600 dark:text-gray-400'>
          <p>
            需要帮助？{' '}
            <a href='#' className='text-primary hover:underline'>
              联系支持
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
