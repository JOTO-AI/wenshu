import {
  Bar,
  CartesianGrid,
  Legend,
  BarChart as RechartsBarChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { ChartContainer } from './chart-container';

export interface BarChartData {
  [key: string]: string | number;
}

export interface BarChartProps {
  data: BarChartData[];
  xDataKey: string;
  bars: {
    dataKey: string;
    fill?: string;
    name?: string;
  }[];
  height?: number;
  className?: string;
  showGrid?: boolean;
  showTooltip?: boolean;
  showLegend?: boolean;
}

export function BarChart({
  data,
  xDataKey,
  bars,
  height = 300,
  className = '',
  showGrid = true,
  showTooltip = true,
  showLegend = true,
}: BarChartProps) {
  const defaultColors = [
    'hsl(var(--primary))',
    'hsl(var(--chart-2))',
    'hsl(var(--chart-3))',
    'hsl(var(--chart-4))',
    'hsl(var(--chart-5))',
  ];

  return (
    <ChartContainer height={height} className={className}>
      <RechartsBarChart data={data}>
        {showGrid && (
          <CartesianGrid
            strokeDasharray='3 3'
            stroke='hsl(var(--border))'
            strokeOpacity={0.3}
          />
        )}
        <XAxis
          dataKey={xDataKey}
          stroke='hsl(var(--muted-foreground))'
          fontSize={12}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke='hsl(var(--muted-foreground))'
          fontSize={12}
          tickLine={false}
          axisLine={false}
        />
        {showTooltip && (
          <Tooltip
            contentStyle={{
              backgroundColor: 'hsl(var(--popover))',
              border: '1px solid hsl(var(--border))',
              borderRadius: 'calc(var(--radius) - 2px)',
              color: 'hsl(var(--popover-foreground))',
            }}
          />
        )}
        {showLegend && <Legend />}
        {bars.map((bar, index) => (
          <Bar
            key={bar.dataKey}
            dataKey={bar.dataKey}
            fill={bar.fill || defaultColors[index % defaultColors.length]}
            name={bar.name || bar.dataKey}
            radius={[4, 4, 0, 0]}
          />
        ))}
      </RechartsBarChart>
    </ChartContainer>
  );
}
