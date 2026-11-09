export interface ColorsDef {
  PRIMARY: string;
  PRIMARY_DARK: string;
  PRIMARY_LIGHT: string;
  PURPLE: string;
  PURPLE_LIGHT: string;
  SUCCESS: string;
  SUCCESS_LIGHT: string;
  WARNING: string;
  WARNING_LIGHT: string;
  ERROR: string;
  ERROR_LIGHT: string;
  BG: string;
  CARD: string;
  TEXT: string;
  TEXT_SECONDARY: string;
  TEXT_LIGHT: string;
  BORDER: string;
  SHADOW: string;
  SHADOW_DARK: string;
}

export const Colors: ColorsDef = {
  PRIMARY: '#3B82F6',
  PRIMARY_DARK: '#2563EB',
  PRIMARY_LIGHT: '#93C5FD',
  PURPLE: '#8B5CF6',
  PURPLE_LIGHT: '#C4B5FD',
  SUCCESS: '#10B981',
  SUCCESS_LIGHT: '#D1FAE5',
  WARNING: '#F59E0B',
  WARNING_LIGHT: '#FEF3C7',
  ERROR: '#EF4444',
  ERROR_LIGHT: '#FEE2E2',
  BG: '#F1F5F9',
  CARD: '#FFFFFF',
  TEXT: '#1E293B',
  TEXT_SECONDARY: '#64748B',
  TEXT_LIGHT: '#94A3B8',
  BORDER: '#E2E8F0',
  SHADOW: '#0000000a',
  SHADOW_DARK: '#00000015',
};

export interface SpacingDef {
  xs: number;
  sm: number;
  md: number;
  lg: number;
  xl: number;
  xxl: number;
}

export const Spacing: SpacingDef = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
};

export interface RadiusDef {
  sm: number;
  md: number;
  lg: number;
  xl: number;
  full: number;
}

export const Radius: RadiusDef = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  full: 999,
};
