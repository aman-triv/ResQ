import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { radius, spacing, tint, typography } from '../theme/theme';
import PulseDot from './PulseDot';

interface BadgeProps {
  label: string;
  color: string;
  showPulse?: boolean;
}

export default function Badge({ label, color, showPulse }: BadgeProps) {
  return (
    <View style={[styles.container, { backgroundColor: tint(color) }]}>
      {showPulse && <PulseDot color={color} size={6} />}
      <Text style={[styles.label, { color }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    paddingHorizontal: spacing.sm,
    paddingVertical: 4,
    borderRadius: radius.pill,
    alignSelf: 'flex-start',
  },
  label: {
    ...typography.small,
    letterSpacing: 0.5,
  },
});
