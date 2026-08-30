import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors, radius, spacing, typography } from '../theme/theme';

interface HeaderProps {
  title: string;
  /** Renders a small solid dot before the title (Home/Jobs use a red one) */
  titleIndicatorColor?: string;
  subtitle: string;
  /** 'shield' = green shield-check icon (e.g. "You are on duty")
   *  'dot'    = plain filled dot (e.g. "Online") */
  subtitleIndicator?: 'shield' | 'dot';
  subtitleColor?: string;
  onMenuPress?: () => void;
  onWalkiePress?: () => void;
}

export default function Header({
  title,
  titleIndicatorColor,
  subtitle,
  subtitleIndicator = 'dot',
  subtitleColor = colors.green,
  onMenuPress,
  onWalkiePress,
}: HeaderProps) {
  const insets = useSafeAreaInsets();

  return (
    <View style={[styles.container, { paddingTop: insets.top + spacing.sm }]}>
      <TouchableOpacity style={styles.iconButton} onPress={onMenuPress} activeOpacity={0.7}>
        <Ionicons name="menu" size={24} color={colors.textPrimary} />
      </TouchableOpacity>

      <View style={styles.centerBlock}>
        <View style={styles.titleRow}>
          {titleIndicatorColor && <View style={[styles.dot, { backgroundColor: titleIndicatorColor }]} />}
          <Text style={styles.title} numberOfLines={1}>
            {title}
          </Text>
        </View>
        <View style={styles.subtitleRow}>
          {subtitleIndicator === 'shield' ? (
            <Ionicons name="shield-checkmark" size={13} color={subtitleColor} />
          ) : (
            <View style={[styles.dot, { backgroundColor: subtitleColor }]} />
          )}
          <Text style={[styles.subtitle, { color: subtitleColor }]}>{subtitle}</Text>
        </View>
      </View>

      <TouchableOpacity style={styles.iconButton} onPress={onWalkiePress} activeOpacity={0.7}>
        <MaterialCommunityIcons name="radio-handheld" size={22} color={colors.textPrimary} />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.md,
    backgroundColor: colors.background,
  },
  iconButton: {
    width: 40,
    height: 40,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
  },
  centerBlock: {
    flex: 1,
    alignItems: 'center',
    gap: 4,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  subtitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  title: {
    ...typography.h3,
    color: colors.textPrimary,
  },
  subtitle: {
    ...typography.caption,
    fontWeight: '600',
  },
});
