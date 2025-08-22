import * as LabelPrimitive from '@radix-ui/react-label';
import { cn } from '@workspace/ui';
import * as React from 'react';

interface LabelProps {
  className?: string;
  children?: React.ReactNode;
  htmlFor?: string;
}

const Label = React.forwardRef<
  HTMLLabelElement,
  LabelProps & React.ComponentPropsWithoutRef<'label'>
>(({ className, children, ...props }, ref) => {
  const Component = LabelPrimitive.Root as any;
  return (
    <Component
      ref={ref}
      data-slot='label'
      className={cn(
        'flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50',
        className
      )}
      {...props}
    >
      {children}
    </Component>
  );
});

Label.displayName = 'Label';

export { Label };
