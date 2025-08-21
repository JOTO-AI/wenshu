import {
  Badge,
  // BarChart,
  Button,
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@workspace/ui';

// 模拟数据 - 暂时未使用但保留供后续图表功能
// const mockUserStats = [
//   { month: '1月', users: 1200, growth: '+15%' },
//   { month: '2月', users: 1380, growth: '+12%' },
//   { month: '3月', users: 1550, growth: '+18%' },
//   { month: '4月', users: 1420, growth: '-8%' },
//   { month: '5月', users: 1680, growth: '+22%' },
//   { month: '6月', users: 1890, growth: '+15%' },
// ];

const mockSystemStats = [
  {
    metric: '总用户数',
    value: '15,234',
    change: '+12.5%',
    status: 'up' as const,
  },
  {
    metric: '活跃用户',
    value: '8,456',
    change: '+8.2%',
    status: 'up' as const,
  },
  {
    metric: '新增用户',
    value: '1,234',
    change: '-2.1%',
    status: 'down' as const,
  },
  {
    metric: '查询次数',
    value: '45,678',
    change: '+25.3%',
    status: 'up' as const,
  },
];

// 暂时未使用但保留供后续活动列表功能
// const mockRecentActivities = [
//   {
//     id: 1,
//     user: '张三',
//     action: '执行SQL查询',
//     time: '2分钟前',
//     status: 'success' as const,
//   },
//   {
//     id: 2,
//     user: '李四',
//     action: '生成数据报表',
//     time: '5分钟前',
//     status: 'success' as const,
//   },
//   {
//     id: 3,
//     user: '王五',
//     action: '创建图表',
//     time: '10分钟前',
//     status: 'pending' as const,
//   },
//   {
//     id: 4,
//     user: '赵六',
//     action: '数据导出',
//     time: '15分钟前',
//     status: 'failed' as const,
//   },
// ];

export function AnalyticsPage() {
  return (
    <div className='space-y-6'>
      {/* 页面标题 */}
      <div>
        <h1 className='text-3xl font-bold tracking-tight'>数据分析</h1>
        <p className='text-muted-foreground'>查看系统使用情况和用户活动统计</p>
      </div>

      {/* 统计卡片 */}
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'>
        {mockSystemStats.map(stat => (
          <Card key={stat.metric}>
            <CardHeader className='pb-2'>
              <CardTitle className='text-sm font-medium text-muted-foreground'>
                {stat.metric}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className='text-2xl font-bold'>{stat.value}</div>
              <div className='flex items-center text-sm'>
                <Badge
                  variant={stat.status === 'up' ? 'default' : 'destructive'}
                  className='text-xs'
                >
                  {stat.change}
                </Badge>
                <span className='ml-2 text-muted-foreground'>
                  {stat.status === 'up' ? '增长' : '下降'}
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* 图表区域 */}
      <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
        {/* 用户增长趋势 */}
        <Card>
          <CardHeader>
            <CardTitle>用户增长趋势</CardTitle>
            <CardDescription>过去6个月的用户增长情况</CardDescription>
          </CardHeader>
          <CardContent>
            {/* Chart temporarily disabled due to component dependencies */}
            <div className='h-[300px] flex items-center justify-center bg-muted/50 rounded-lg'>
              <p className='text-muted-foreground'>图表组件暂时不可用</p>
            </div>
            {/* <ChartContainer height={300} className='w-full'>
              <LineChart
                data={mockUserStats.map(item => ({
                  name: item.month,
                  value: item.users,
                }))}
                xDataKey='name'
                lines={[{ dataKey: 'value', stroke: '#8884d8' }]}
              />
            </ChartContainer> */}
          </CardContent>
        </Card>

        {/* 活动统计 */}
        <Card>
          <CardHeader>
            <CardTitle>月度活动统计</CardTitle>
            <CardDescription>各月用户活动对比</CardDescription>
          </CardHeader>
          <CardContent>
            {/* Chart temporarily disabled due to component dependencies */}
            <div className='h-[300px] flex items-center justify-center bg-muted/50 rounded-lg'>
              <p className='text-muted-foreground'>图表组件暂时不可用</p>
            </div>
            {/* <ChartContainer height={300} className='w-full'>
              <BarChart
                data={mockUserStats.map(item => ({
                  name: item.month,
                  value: item.users,
                }))}
                xDataKey='name'
                bars={[{ dataKey: 'value', fill: '#8884d8' }]}
              />
            </ChartContainer> */}
          </CardContent>
        </Card>
      </div>

      {/* 最近活动表格 */}
      <Card>
        <CardHeader className='flex flex-row items-center justify-between'>
          <div>
            <CardTitle>最近活动</CardTitle>
            <CardDescription>用户最近的系统操作记录</CardDescription>
          </div>
          <Button variant='outline' size='sm'>
            查看全部
          </Button>
        </CardHeader>
        <CardContent>
          {/* Table temporarily disabled due to component dependencies */}
          <div className='text-center text-muted-foreground py-8'>
            表格组件暂时不可用，正在解决依赖问题...
          </div>
          {/* <Table>
            <TableHeader>
              <TableRow>
                <TableHead>用户</TableHead>
                <TableHead>操作</TableHead>
                <TableHead>时间</TableHead>
                <TableHead>状态</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockRecentActivities.map(activity => (
                <TableRow key={activity.id}>
                  <TableCell className='font-medium'>{activity.user}</TableCell>
                  <TableCell>{activity.action}</TableCell>
                  <TableCell className='text-muted-foreground'>
                    {activity.time}
                  </TableCell>
                  <TableCell>
                    <Badge
                      variant={
                        activity.status === 'success'
                          ? 'default'
                          : activity.status === 'pending'
                          ? 'secondary'
                          : 'destructive'
                      }
                    >
                      {activity.status === 'success'
                        ? '成功'
                        : activity.status === 'pending'
                        ? '处理中'
                        : '失败'}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table> */}
        </CardContent>
      </Card>
    </div>
  );
}

export default AnalyticsPage;
