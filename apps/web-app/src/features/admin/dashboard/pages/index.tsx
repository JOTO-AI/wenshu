/**
 * 管理端数据仪表板页面
 * 显示系统概览统计和主要数据指标
 */
function DashboardPage() {
  return (
    <div
      style={{
        padding: '20px',
        backgroundColor: '#f0f0f0',
        minHeight: '400px',
        border: '2px solid #ff0000',
      }}
    >
      <h1
        style={{
          fontSize: '24px',
          color: '#ff0000',
          marginBottom: '20px',
        }}
      >
        🔴 测试：Dashboard 页面内容
      </h1>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '16px',
          marginBottom: '20px',
        }}
      >
        <div
          style={{
            backgroundColor: '#e0e0e0',
            padding: '40px',
            borderRadius: '8px',
            textAlign: 'center',
          }}
        >
          📊 用户统计
        </div>
        <div
          style={{
            backgroundColor: '#e0e0e0',
            padding: '40px',
            borderRadius: '8px',
            textAlign: 'center',
          }}
        >
          📈 查询统计
        </div>
        <div
          style={{
            backgroundColor: '#e0e0e0',
            padding: '40px',
            borderRadius: '8px',
            textAlign: 'center',
          }}
        >
          ⚡ 系统状态
        </div>
      </div>

      <div
        style={{
          backgroundColor: '#d0d0d0',
          padding: '60px',
          borderRadius: '8px',
          textAlign: 'center',
          fontSize: '18px',
        }}
      >
        📋 主要数据图表区域 - 如果您看到这个内容，说明页面渲染正常
      </div>
    </div>
  );
}

export default DashboardPage;
