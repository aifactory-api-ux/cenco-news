import React, { SelectHTMLAttributes } from 'react';
import { tokens } from '../../styles/tokens';

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
}

export default function Select({ label, error, id, className, children, ...props }: SelectProps) {
  const selectClasses = `w-full rounded-md border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary_blue ${error ? 'border-danger_red' : 'border-secondary_text_border'}`;

  return (
    <div className={className} style={{ fontFamily: tokens.typography.font_family }}>
      <label htmlFor={id} className="block mb-1 font-semibold text-neutral_text">
        {label}
      </label>
      <select id={id} className={selectClasses} {...props}>
        {children}
      </select>
      {error && <p className="mt-1 text-danger_red text-sm">{error}</p>}
    </div>
  );
}
