import React from 'react';
import { TouchableOpacity, Text, View, StyleSheet, StyleProp, ViewStyle } from 'react-native';
import { Ionicons, MaterialCommunityIcons, FontAwesome5 } from '@expo/vector-icons';
import { colors, radius, spacing, typography } from '../theme/theme';

type IconSet = 'ionicons' | 'material-community' | 'font-awesome-5';
type Variant = 'full' | 'grid' | 'hero';

interface ActionButtonProps {
  label: string;
  subLabel?: string;
  iconName: string;
  iconSet?: IconSet;
  color: string;
  variant?: Variant;
  /** true (default): solid `color` background, white icon/text — used for
   *  Home's status buttons and Admin SOS.
   *  false: dark card background with a `color`-tinted icon — used for
   *  the Chat screen's Quick Actions row. */
  filled?: boolean;
  onPress?: () => void;
  style?: StyleProp<ViewStyle>;
  disabled?: boolean;
}

export default function ActionButton({
  label,
  subLabel,
  iconName,
  iconSet = 'ionicons',
  color,
  variant = 'grid',
  filled = true,
  onPress,
  style,
  disabled,
}: ActionButtonProps) {
  const IconComponent =
    iconSet === 'material-community' ? MaterialCommunityIcons : iconSet === 'font-awesome-5' ? FontAwesome5 : Ionicons;
  // FontAwesome5's "free" glyphs (procedures, thumbtack, plus, etc.) only exist
  // in the solid weight — without this they render blank.
  const iconExtraProps = iconSet === 'font-awesome-5' ? { solid: true } : {};
  const backgroundColor = filled ? color : colors.surfaceElevated;
  const contentColor = filled ? colors.white : color;
  const labelColor = filled ? colors.white : colors.textPrimary;
  const iconSize = variant === 'hero' ? 28 : iconSet === 'font-awesome-5' ? 20 : 24;

  return (
    <TouchableOpacity
      activeOpacity={0.8}
      onPress={onPress}
      disabled={disabled}
      style={[
        styles.base,
        variant === 'full' && styles.full,
        variant === 'grid' && styles.grid,
        variant === 'hero' && styles.hero,
        { backgroundColor, opacity: disabled ? 0.5 : 1 },
        style,
      ]}
    >
      {variant === 'hero' ? (
        <>
          <IconComponent name={iconName as any} size={iconSize} color={contentColor} {...iconExtraProps} />
          <View style={styles.heroTextWrap}>
            <Text style={[styles.heroLabel, { color: labelColor }]}>{label}</Text>
            {!!subLabel && <Text style={[styles.heroSub, { color: labelColor }]}>{subLabel}</Text>}
          </View>
        </>
      ) : variant === 'full' ? (
        <>
          <IconComponent name={iconName as any} size={iconSize} color={contentColor} {...iconExtraProps} />
          <Text style={[styles.fullLabel, { color: labelColor }]}>{label}</Text>
        </>
      ) : (
        <>
          <IconComponent name={iconName as any} size={iconSize} color={contentColor} {...iconExtraProps} />
          <Text style={[styles.gridLabel, { color: labelColor }]} numberOfLines={2}>
            {label}
          </Text>
        </>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  base: {
    borderRadius: radius.lg,
    alignItems: 'center',
    justifyContent: 'center',
  },
  full: {
    flexDirection: 'row',
    gap: spacing.sm,
    paddingVertical: spacing.lg,
  },
  fullLabel: {
    ...typography.h3,
    letterSpacing: 0.5,
  },
  grid: {
    flex: 1,
    paddingVertical: spacing.md,
    gap: spacing.xs,
  },
  gridLabel: {
    ...typography.caption,
    fontWeight: '700',
    textAlign: 'center',
  },
  hero: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    paddingVertical: spacing.lg,
    paddingHorizontal: spacing.lg,
    justifyContent: 'flex-start',
  },
  heroTextWrap: {
    alignItems: 'flex-start',
  },
  heroLabel: {
    ...typography.h3,
  },
  heroSub: {
    ...typography.caption,
    opacity: 0.85,
  },
});
