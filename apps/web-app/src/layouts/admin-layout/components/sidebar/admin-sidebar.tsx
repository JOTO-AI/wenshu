import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from '@workspace/ui';
import * as React from 'react';
import { adminMenuData } from '../../constants/menu-data';
import { NavMain } from './nav-main';
import { NavUser } from './nav-user';
import { TeamSwitcher } from './team-switcher';

export function AdminSidebar({
  ...props
}: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible='icon' {...props}>
      <SidebarHeader>
        <TeamSwitcher system={adminMenuData.system} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={adminMenuData.navMain} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={adminMenuData.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
