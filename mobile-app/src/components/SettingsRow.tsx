import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, tint, typography } from '../theme/theme';
import type { SettingsItem } from '../types/models';

export default function SettingsRow({ item, isLast }: { item: SettingsItem; isLast?: boolean }) {
  return (
    <TouchableOpacity
      activeOpacity={0.7}
      style={[styles.row, !isLast && styles.rowDivider]}
    >
      <View style={[styles.iconWrap, { backgroundColor: tint(item.iconColor) }]}>
        <Ionicons name={item.icon as any} size={19} color={item.iconColor} />
      </View>
      <View style={styles.textCol}>
        <Text style={styles.title}>{item.title}</Text>
        <Text style={styles.subtitle} numberOfLines={1}>
          {item.subtitle}
        </Text>
      </View>
      <Ionicons name="chevron-forward" size={18} color={colors.textTertiary} />
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    paddingVertical: spacing.md,
  },
  rowDivider: {
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  iconWrap: {
    width: 38,
    height: 38,
    borderRadius: 19,
    alignItems: 'center',
    justifyContent: 'center',
  },
  textCol: {
    flex: 1,
    gap: 2,
  },
  title: {
    ...typography.bodyBold,
    color: colors.textPrimary,
  },
  subtitle: {
    ...typography.caption,
    color: colors.textSecondary,
  },
});
