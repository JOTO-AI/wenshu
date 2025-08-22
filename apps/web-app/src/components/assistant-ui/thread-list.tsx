// import React from "react"; // 不需要显式导入React
import { ArchiveIcon, PlusIcon } from "lucide-react";

import { Button } from "@workspace/ui";
import { TooltipIconButton } from "./tooltip-icon-button";

export const ThreadList = () => {
  return (
    <div className="aui-root aui-thread-list-root h-full">
      <div className="mb-4">
        <ThreadListNew />
      </div>
      <div className="flex-1 overflow-y-auto">
        <ThreadListItems />
      </div>
    </div>
  );
};

const ThreadListNew = () => {
  return (
    <Button 
      className="aui-thread-list-new w-full justify-start" 
      variant="outline" 
      size="sm"
    >
      <PlusIcon className="h-4 w-4 mr-2" />
      New Conversation
    </Button>
  );
};

const ThreadListItems = () => {
  // 模拟聊天历史数据
  const mockThreads = [
    { id: 1, title: '数据分析报告', time: '2小时前', active: true },
    { id: 2, title: '用户增长趋势分析', time: '1天前', active: false },
    { id: 3, title: '销售业绩仪表板', time: '3天前', active: false },
    { id: 4, title: '系统性能指标查询', time: '1周前', active: false },
    { id: 5, title: '月度数据报表', time: '2周前', active: false },
  ];

  return (
    <div className="space-y-1">
      {mockThreads.map((thread) => (
        <ThreadListItem key={thread.id} thread={thread} />
      ))}
    </div>
  );
};

const ThreadListItem = ({ thread }: { thread: { id: number; title: string; time: string; active: boolean } }) => {
  return (
    <div className={`
      aui-thread-list-item group flex items-center gap-2 p-3 rounded-lg cursor-pointer
      transition-colors duration-200
      ${thread.active 
        ? 'bg-primary/10 border border-primary/20' 
        : 'hover:bg-muted/60'
      }
    `}>
      <button className="aui-thread-list-item-trigger flex-1 text-left">
        <ThreadListItemTitle title={thread.title} time={thread.time} />
      </button>
      <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-200">
        <ThreadListItemArchive />
      </div>
    </div>
  );
};

const ThreadListItemTitle = ({ title, time }: { title: string; time: string }) => {
  return (
    <div className="aui-thread-list-item-title">
      <p className="text-sm font-medium truncate mb-1">
        {title}
      </p>
      <p className="text-xs text-muted-foreground">
        {time}
      </p>
    </div>
  );
};

const ThreadListItemArchive = () => {
  return (
    <TooltipIconButton
      className="aui-thread-list-item-archive h-8 w-8"
      variant="ghost"
      size="icon"
      tooltip="Archive conversation"
    >
      <ArchiveIcon className="h-3 w-3" />
    </TooltipIconButton>
  );
};