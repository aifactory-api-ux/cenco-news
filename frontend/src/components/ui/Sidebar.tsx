// src/components/ui/Sidebar.tsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import { LucideIcon, Home, FileText, Settings, Users, Bell, PieChart } from 'lucide-react';

const menuItems = [
  { to: '/', icon: Home, label: 'Dashboard' },
  { to: '/news', icon: FileText, label: 'Noticias' },
  { to: '/sources', icon: Settings, label: 'Fuentes' },
  { to: '/scoring', icon: PieChart, label: 'Scoring' },
  { to: '/reports', icon: FileText, label: 'Reportes' },
  { to: '/recipients', icon: Users, label: 'Destinatarios' },
  { to: '/channels', icon: Bell, label: 'Canales' },
  { to: '/audit', icon: Settings, label: 'Auditoría' },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-[#E0F2F7] min-h-screen flex flex-col shadow-md">
      <div className="p-6 font-semibold text-[#0056B3] text-xl">CENCO NEWS</div>
      <nav className="flex flex-col gap-2 p-4">
        {menuItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            to={to}
            key={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-2 rounded-md transition-colors duration-200 hover:bg-[#0056B3] hover:text-white ${
                isActive ? 'bg-[#0056B3] text-white font-semibold' : 'text-[#0056B3]'
              }`
            }
            end
          >
            <Icon className="w-5 h-5" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
