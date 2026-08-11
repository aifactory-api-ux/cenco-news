const colors = require('tailwindcss/colors');
const designTokens = {
  primaryBlue: '#0056B3',
  darkBlueAccent: '#003366',
  lightBlueBackground: '#E0F2F7',
  neutralText: '#333333',
  secondaryTextBorder: '#CCCCCC',
  backgroundWhite: '#FFFFFF',
  successGreen: '#28A745',
  dangerRed: '#DC3545'
};

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./frontend/src/**/*.{tsx,ts,jsx,js}'],
  theme: {
    extend: {
      colors: {
        primaryBlue: designTokens.primaryBlue,
        darkBlueAccent: designTokens.darkBlueAccent,
        lightBlueBackground: designTokens.lightBlueBackground,
        neutralText: designTokens.neutralText,
        secondaryTextBorder: designTokens.secondaryTextBorder,
        backgroundWhite: designTokens.backgroundWhite,
        successGreen: designTokens.successGreen,
        dangerRed: designTokens.dangerRed
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      fontWeight: {
        semibold: '600',
        medium: '500',
        regular: '400',
      },
      fontSize: {
        h1: ['32px', { lineHeight: '1.2' }],
        h2: ['24px', { lineHeight: '1.2' }],
        h3: ['20px', { lineHeight: '1.3' }],
        bodyLarge: ['16px', { lineHeight: '1.5' }],
        bodyRegular: ['14px', { lineHeight: '1.5' }],
        smallText: ['12px', { lineHeight: '1.4' }],
      },
      spacing: {
        baseUnit: '8px',
        spaceXs: '4px',
        spaceSm: '8px',
        spaceMd: '16px',
        spaceLg: '24px',
        spaceXl: '32px',
        spaceXxl: '48px',
      },
      borderRadius: {
        radiusSm: '4px',
        radiusMd: '8px',
        radiusLg: '12px',
      },
      boxShadow: {
        shadowSm: '0px 1px 3px rgba(0, 0, 0, 0.1)',
        shadowMd: '0px 4px 6px rgba(0, 0, 0, 0.1)',
      },
    },
  },
  plugins: [],
};
