import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { colors, radius, shadow, spacing, typography } from '../theme/theme';
import type { SOSAlert } from '../types/models';

interface SOSAlertCardProps {
  alert: SOSAlert;
  onAccept?: () => void;
  onIgnore?: () => void;
}

export default function SOSAlertCard({ alert, onAccept, onIgnore }: SOSAlertCardProps) {
  return (
    <LinearGradient
      colors={[colors.red, colors.redDark]}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={styles.card}
    >
      <View style={styles.topRow}>
        <View style={styles.bellWrap}>
          <Ionicons name="notifications" size={14} color={colors.white} />
        </View>
        <Text style={styles.alertTag}>NEW SOS ALERT</Text>
        <Text style={styles.time}>{alert.timeLabel}</Text>
      </View>

      <View style={styles.titleRow}>
        <Text style={styles.title}>{alert.title}</Text>
        <Ionicons name="pulse" size={30} color="rgba(255,255,255,0.9)" />
      </View>

      <View style={styles.locationRow}>
        <Ionicons name="location-sharp" size={14} color="rgba(255,255,255,0.85)" />
        <Text style={styles.locationText}>{alert.location}</Text>
      </View>
      <Text style={styles.meta}>{alert.meta}</Text>

      <View style={styles.divider} />

      <View style={styles.buttonsRow}>
        <TouchableOpacity style={styles.acceptBtn} onPress={onAccept} activeOpacity={0.85}>
          <Ionicons name="checkmark-circle" size={18} color={colors.red} />
          <Text style={styles.acceptText}>ACCEPT</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.ignoreBtn} onPress={onIgnore} activeOpacity={0.85}>
          <Ionicons name="close-circle-outline" size={18} color={colors.white} />
          <Text style={styles.ignoreText}>IGNORE</Text>
        </TouchableOpacity>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: radius.xl,
    padding: spacing.lg,
    ...shadow.floating,
  },
  topRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  bellWrap: {
    width: 26,
    height: 26,
    borderRadius: 13,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  alertTag: {
    ...typography.small,
    color: colors.white,
    backgroundColor: 'rgba(0,0,0,0.2)',
    paddingHorizontal: spacing.sm,
    paddingVertical: 3,
    borderRadius: radius.sm,
    letterSpacing: 0.5,
  },
  time: {
    ...typography.caption,
    color: 'rgba(255,255,255,0.8)',
    marginLeft: 'auto',
  },
  titleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: spacing.md,
    marginBottom: spacing.sm,
  },
  title: {
    ...typography.h2,
    color: colors.white,
    flex: 1,
  },
  locationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    marginBottom: 4,
  },
  locationText: {
    ...typography.body,
    color: 'rgba(255,255,255,0.9)',
  },
  meta: {
    ...typography.caption,
    color: 'rgba(255,255,255,0.85)',
  },
  divider: {
    height: 1,
    backgroundColor: 'rgba(255,255,255,0.25)',
    marginVertical: spacing.md,
  },
  buttonsRow: {
    flexDirection: 'row',
    gap: spacing.md,
  },
  acceptBtn: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.xs,
    backgroundColor: colors.white,
    paddingVertical: spacing.md,
    borderRadius: radius.md,
  },
  acceptText: {
    ...typography.bodyBold,
    color: colors.red,
    letterSpacing: 0.5,
  },
  ignoreBtn: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.xs,
    backgroundColor: 'rgba(0,0,0,0.15)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.4)',
    paddingVertical: spacing.md,
    borderRadius: radius.md,
  },
  ignoreText: {
    ...typography.bodyBold,
    color: colors.white,
    letterSpacing: 0.5,
  },
});
