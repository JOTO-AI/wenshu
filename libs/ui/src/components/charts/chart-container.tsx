import { ReactElement } from 'react';
import { ResponsiveContainer } from 'recharts';

export interface ChartContainerProps {
  children: ReactElement;
  width?: string | number;
  height?: number;
  className?: string;
}

export function ChartContainer({
  children,
  width = '100%',
  height = 300,
  className = '',
}: ChartContainerProps) {
  return (
    <div className={`w-full ${className}`} style={{ minHeight: height }}>
      <ResponsiveContainer width={width} height={height}>
        {children}
      </ResponsiveContainer>
    </div>
  );
}
