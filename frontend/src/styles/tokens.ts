// frontend/src/styles/tokens.ts

export const tokens = {
  colors: {
    primary: {
      500: '#007BFF',
      600: '#0056B3'
    },
    secondary: {
      500: '#28A745',
      600: '#1E7E34'
    },
    neutral: {
      100: '#F8F9FA',
      200: '#E9ECEF',
      500: '#ADB5BD',
      700: '#495057',
      900: '#212529'
    },
    feedback: {
      error: '#DC3545',
      warning: '#FFC107'
    }
  },
  typography: {
    font_family: "'Inter', sans-serif",
    base_size: '16px',
    line_height: 1.5,
    headings: {
      h1: {
        font_size: '32px',
        font_weight: 'bold'
      },
      h2: {
        font_size: '24px',
        font_weight: 'semibold'
      },
      h3: {
        font_size: '20px',
        font_weight: 'semibold'
      }
    },
    small_text: {
      font_size: '14px',
      font_weight: 'regular'
    }
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px'
  },
  radii: {
    sm: '4px',
    md: '8px'
  },
  shadows: {
    sm: '0px 1px 3px rgba(0, 0, 0, 0.1)',
    md: '0px 4px 6px rgba(0, 0, 0, 0.1)'
  },
  icon_image_style: {
    icons: 'Estilo de línea, minimalista, monocromático (usando neutral-700).',
    images: 'Profesionales, relevantes al contexto de noticias/inteligencia, sin elementos distractores.'
  },
  motion_interaction: {
    transitions: 'Transiciones suaves (ease-in-out, 150ms) para estados de hover, focus y cambios de visibilidad.',
    loading_indicators: 'Indicadores de carga discretos (spinners, barras de progreso).'
  }
};
