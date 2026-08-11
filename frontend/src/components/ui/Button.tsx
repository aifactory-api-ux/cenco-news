import React, { ButtonHTMLAttributes, ReactNode } from 'react';
import { tokens } from '../../styles/tokens';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary';
}

export default function Button({ children, variant = 'primary', disabled, className, ...props }: ButtonProps) {
  const baseClasses = 'rounded-md px-4 py-2 font-semibold focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variantClasses = {
    primary: `bg-primary_blue text-white hover:bg-dark_blue_accent focus:ring-primary_blue disabled:opacity-50 disabled:cursor-not-allowed`,
    secondary: `bg-secondary_text_border text-neutral_text hover:bg-light_blue_background focus:ring-secondary_text_border disabled:opacity-50 disabled:cursor-not-allowed`,
  };

  const combinedClasses = `${baseClasses} ${variantClasses[variant]} ${className ?? ''}`;

  return (
    <button className={combinedClasses} disabled={disabled} {...props} />
  );
}
