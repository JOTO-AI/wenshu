declare module '@assistant-ui/react' {
  import React from 'react';

  // Runtime Provider
  export interface AssistantRuntimeProviderProps {
    runtime: any;
    children: React.ReactNode;
  }
  export const AssistantRuntimeProvider: React.FC<AssistantRuntimeProviderProps>;

  // Thread Primitives
  export namespace ThreadPrimitive {
    export const Root: React.FC<React.HTMLAttributes<HTMLDivElement> & { className?: string }>;
    export const Viewport: React.FC<React.HTMLAttributes<HTMLDivElement> & { className?: string }>;
    export const Empty: React.FC<{ children: React.ReactNode }>;
    export const Messages: React.FC<{ components: { UserMessage: React.ComponentType; AssistantMessage: React.ComponentType } }>;
    export const ScrollToBottom: React.FC<{ asChild?: boolean; children?: React.ReactNode }>;
    export const If: React.FC<{ running?: boolean; children: React.ReactNode }>;
    export const Suggestion: React.FC<{ 
      prompt: string; 
      method?: string; 
      asChild?: boolean; 
      children?: React.ReactNode; 
    }>;
  }

  // Message Primitives
  export namespace MessagePrimitive {
    export const Root: React.FC<React.HTMLAttributes<HTMLDivElement> & { className?: string }>;
    export const Content: React.FC<React.HTMLAttributes<HTMLDivElement>>;
  }

  // Composer Primitives
  export namespace ComposerPrimitive {
    export const Root: React.FC<React.HTMLAttributes<HTMLDivElement> & { className?: string }>;
    export const Input: React.FC<React.TextareaHTMLAttributes<HTMLTextAreaElement> & { 
      autoFocus?: boolean;
      placeholder?: string;
      className?: string;
    }>;
    export const Send: React.FC<{ asChild?: boolean; children?: React.ReactNode }>;
  }
}
