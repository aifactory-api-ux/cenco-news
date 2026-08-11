import React from 'react';
import { Bell } from 'lucide-react';
import { tokens } from '../../styles/tokens';

export default function Header() {
  return (
    <header
      className="flex items-center justify-between px-6 py-4 shadow-md"
      style={{ backgroundColor: tokens.colors.background_white, boxShadow: tokens.shadows.shadow_md }}
    >
      <div style={{ fontFamily: tokens.typography.font_family }} className="text-xl font-semibold text-primary_blue">
        CENCO NEWS
      </div>

      <div className="flex items-center space-x-4">
        {/* Notifications icon */}
        <button
          aria-label="Notificaciones"
          className="text-neutral_text hover:text-primary_blue transition-colors"
        >
          <Bell size={24} />
        </button>

        {/* User profile placeholder */}
        <div
          className="w-10 h-10 rounded-full bg-primary_blue text-white flex items-center justify-center select-none"
          style={{ fontFamily: tokens.typography.font_family }}
        >
          {/* Initials or user icon could go here */}
          US
        </div>
      </div>
    </header>
  );
}
