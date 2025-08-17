import {
  CartesianGrid,
  Legend,
  Line,
  LineChart as RechartsLineChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { ChartContainer } from './chart-container';

export interface LineChartData {
  [key: string]: string | number;
}

export interface LineChartProps {
  data: LineChartData[];
  xDataKey: string;
  lines: {
    dataKey: string;
    stroke?: string;
    name?: string;
  }[];
  height?: number;
  className?: string;
  showGrid?: boolean;
  showTooltip?: boolean;
  showLegend?: boolean;
}

export function LineChart({
  data,
  xDataKey,
  lines,
  height = 300,
  className = '',
  showGrid = true,
  showTooltip = true,
  showLegend = true,
}: LineChartProps) {
  const defaultColors = [
    'hsl(var(--primary))',
    'hsl(var(--chart-2))',
    'hsl(var(--chart-3))',
    'hsl(var(--chart-4))',
    'hsl(var(--chart-5))',
  ];

  return (
    <ChartContainer height={height} className={className}>
      <RechartsLineChart data={data}>
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
        {lines.map((line, index) => (
          <Line
            key={line.dataKey}
            type='monotone'
            dataKey={line.dataKey}
            stroke={line.stroke || defaultColors[index % defaultColors.length]}
            name={line.name || line.dataKey}
            strokeWidth={2}
            dot={{
              fill: line.stroke || defaultColors[index % defaultColors.length],
              strokeWidth: 2,
              r: 4,
            }}
            activeDot={{ r: 6 }}
          />
        ))}
      </RechartsLineChart>
    </ChartContainer>
  );
}
