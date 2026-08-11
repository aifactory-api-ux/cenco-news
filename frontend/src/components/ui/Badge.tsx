import React from 'react';
import { tokens } from '../../styles/tokens';

interface BadgeProps {
  status: 'pending' | 'approved' | 'rejected';
}

export default function Badge({ status }: BadgeProps) {
  const colors = {
    pending: {
      background: tokens.colors.light_blue_background,
      text: tokens.colors.neutral_text,
    },
    approved: {
      background: tokens.colors.success_green,
      text: tokens.colors.background_white,
    },
    rejected: {
      background: tokens.colors.danger_red,
      text: tokens.colors.background_white,
    },
  };

  const { background, text } = colors[status] || colors.pending;

  return (
    <span
      className="inline-block px-3 py-1 rounded-full font-semibold text-sm"
      style={{ backgroundColor: background, color: text, fontFamily: tokens.typography.font_family }}
    >
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}
