import { Button, Input, cn } from '@workspace/ui';
import * as React from 'react';
import { Label } from './label';

interface LoginFormProps
  extends Omit<React.ComponentProps<'form'>, 'onSubmit'> {
  onSubmit?: (data: { email: string; password: string }) => void;
  onSSOLogin?: (provider: string) => void;
  loading?: boolean;
}

export function LoginForm({
  className,
  onSubmit,
  onSSOLogin,
  loading = false,
  ...props
}: LoginFormProps) {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit?.({ email, password });
  };

  return (
    <form
      className={cn('flex flex-col gap-6', className)}
      onSubmit={handleSubmit}
      {...props}
    >
      <div className='flex flex-col items-center gap-2 text-center'>
        <h1 className='text-2xl font-bold'>登录到您的账户</h1>
        <p className='text-muted-foreground text-sm text-balance'>
          输入您的电子邮件以登录到您的账户
        </p>
      </div>

      <div className='grid gap-6'>
        {/* Email Input */}
        <div className='grid gap-3'>
          <Label htmlFor='email'>电子邮件</Label>
          <Input
            id='email'
            type='email'
            placeholder='m@example.com'
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        {/* Password Input */}
        <div className='grid gap-3'>
          <div className='flex items-center'>
            <Label htmlFor='password'>密码</Label>
            <a
              href='#'
              className='ml-auto text-sm underline-offset-4 hover:underline'
            >
              忘记您的密码？
            </a>
          </div>
          <Input
            id='password'
            type='password'
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        {/* Login Button */}
        <Button type='submit' className='w-full' disabled={loading}>
          {loading ? '登录中...' : '登录'}
        </Button>

        {/* Divider */}
        <div className='after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t'>
          <span className='bg-background text-muted-foreground relative z-10 px-2'>
            或者继续使用
          </span>
        </div>

        {/* SSO Buttons */}
        <div className='grid gap-3'>
          <Button
            type='button'
            variant='outline'
            className='w-full'
            onClick={() => onSSOLogin?.('sso')}
            disabled={loading}
          >
            使用SSO登录
          </Button>
        </div>
      </div>

      <div className='text-center text-sm'>
        没有账户？{' '}
        <a href='#' className='underline underline-offset-4'>
          注册
        </a>
      </div>
    </form>
  );
}
