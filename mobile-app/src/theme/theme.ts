/**
 * Central design tokens for the Emergency Rescue Team app.
 *
 * Strict dark theme, per spec:
 *  - Background: deep charcoal/black
 *  - Accents: Emergency Red / Success Green / Warning Orange / Action Blue
 *
 * `purple` is one addition beyond the brief's four core accents — the
 * Profile screen mockup uses it for the "Distance" stat and "Help &
 * Support" icon, so it's promoted to a first-class token rather than
 * a one-off inline hex value.
 *
 * Every screen and component should pull from here instead of hardcoding
 * hex values, so the whole app stays visually consistent by construction.
 */

export const colors = {
  // Backgrounds
  background: '#121212',
  surface: '#1E1E1E',
  surfaceElevated: '#242424',
  card: '#1A1A1A',
  border: '#2C2C2E',
  overlay: 'rgba(0,0,0,0.55)',

  // Text
  textPrimary: '#FFFFFF',
  textSecondary: '#9CA3AF',
  textTertiary: '#6B7280',

  // Brand / semantic accents
  red: '#EF4444',
  redDark: '#B91C1C',
  green: '#22C55E',
  greenDark: '#15803D',
  orange: '#F59E0B',
  blue: '#3B82F6',
  purple: '#A855F7',
  teal: '#14B8A6',

  white: '#FFFFFF',
  black: '#000000',
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
  xxxl: 32,
} as const;

export const radius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  pill: 999,
} as const;

export const typography = {
  h1: { fontSize: 24, fontWeight: '700' as const },
  h2: { fontSize: 20, fontWeight: '700' as const },
  h3: { fontSize: 16, fontWeight: '700' as const },
  bodyBold: { fontSize: 15, fontWeight: '600' as const },
  body: { fontSize: 14, fontWeight: '400' as const },
  caption: { fontSize: 13, fontWeight: '400' as const },
  small: { fontSize: 11, fontWeight: '600' as const },
} as const;

export const shadow = {
  card: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  floating: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.45,
    shadowRadius: 16,
    elevation: 12,
  },
} as const;

// Alpha-tinted background for a given accent, used behind badges/icons
// e.g. tint(colors.green, '26') -> '#22C55E26' (~15% opacity)
export function tint(hexColor: string, alphaHex: string = '26') {
  return `${hexColor}${alphaHex}`;
}
