import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, radius, spacing, tint, typography } from '../theme/theme';
import type { ResponderStat } from '../types/models';

export default function StatCard({ stat }: { stat: ResponderStat }) {
  return (
    <View style={styles.card}>
      <View style={styles.topRow}>
        <View style={[styles.iconWrap, { backgroundColor: tint(stat.color) }]}>
          <Ionicons name={stat.icon as any} size={18} color={stat.color} />
        </View>
        <Text style={styles.label} numberOfLines={1}>
          {stat.label}
        </Text>
      </View>
      <Text style={styles.value}>{stat.value}</Text>
      <Text style={[styles.sublabel, { color: stat.color }]}>{stat.sublabel}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    flexBasis: '48%',
    flexGrow: 1,
    backgroundColor: colors.card,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
  },
  topRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  iconWrap: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  label: {
    ...typography.caption,
    color: colors.textSecondary,
    flexShrink: 1,
  },
  value: {
    ...typography.h1,
    color: colors.textPrimary,
    marginBottom: 2,
  },
  sublabel: {
    ...typography.small,
  },
});
