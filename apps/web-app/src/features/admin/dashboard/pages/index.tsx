import { Card, CardContent, CardHeader, CardTitle } from '@workspace/ui';

/**
 * 管理端数据仪表板页面
 * 显示系统概览统计和主要数据指标
 */
function DashboardPage() {
  return (
    <div className='p-6 space-y-6'>
      <div className='border-l-4 border-primary bg-primary/10 p-4 rounded-md'>
        <h1 className='text-2xl font-bold text-primary mb-2'>📊 数据仪表板</h1>
        <p className='text-muted-foreground'>系统概览统计和主要数据指标</p>
      </div>

      <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
        <Card>
          <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
            <CardTitle className='text-sm font-medium'>用户统计</CardTitle>
            <span className='text-2xl'>📊</span>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold'>2,345</div>
            <p className='text-xs text-muted-foreground'>活跃用户数</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
            <CardTitle className='text-sm font-medium'>查询统计</CardTitle>
            <span className='text-2xl'>📈</span>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold'>12,678</div>
            <p className='text-xs text-muted-foreground'>今日查询次数</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
            <CardTitle className='text-sm font-medium'>系统状态</CardTitle>
            <span className='text-2xl'>⚡</span>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold text-green-600'>正常</div>
            <p className='text-xs text-muted-foreground'>系统运行状态</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>主要数据图表区域</CardTitle>
        </CardHeader>
        <CardContent>
          <div className='flex items-center justify-center h-64 bg-muted/50 rounded-md'>
            <div className='text-center'>
              <span className='text-4xl mb-2 block'>📋</span>
              <p className='text-lg font-medium'>图表组件开发中</p>
              <p className='text-sm text-muted-foreground'>
                这里将显示详细的数据可视化图表
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default DashboardPage;
