import React, { InputHTMLAttributes } from 'react';
import { tokens } from '../../styles/tokens';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export default function Input({ label, error, id, className, ...props }: InputProps) {
  const inputClasses = `w-full rounded-md border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary_blue ${error ? 'border-danger_red' : 'border-secondary_text_border'}`;

  return (
    <div className={className} style={{ fontFamily: tokens.typography.font_family }}>
      <label htmlFor={id} className="block mb-1 font-semibold text-neutral_text">
        {label}
      </label>
      <input id={id} className={inputClasses} {...props} />
      {error && <p className="mt-1 text-danger_red text-sm">{error}</p>}
    </div>
  );
}
