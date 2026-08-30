import React from 'react';
import { View, Text, Image, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import Header from '../components/Header';
import StatCard from '../components/StatCard';
import SettingsRow from '../components/SettingsRow';
import { colors, radius, shadow, spacing, typography } from '../theme/theme';
import { responderProfile, responderStats, settingsItems } from '../data/mockData';

export default function ProfileScreen() {
  return (
    <View style={styles.container}>
      <Header title="Responder Profile" subtitle="Online" subtitleIndicator="dot" />

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <View style={styles.profileCard}>
          <View style={styles.profileTopRow}>
            <Image source={{ uri: responderProfile.avatarUrl }} style={styles.avatar} />
            <View style={styles.profileInfo}>
              <View style={styles.nameRow}>
                <Text style={styles.name}>{responderProfile.name}</Text>
                <Ionicons name="shield-checkmark" size={16} color={colors.green} />
              </View>
              <Text style={styles.badgeLabel}>Badge ID</Text>
              <Text style={styles.badgeValue}>{responderProfile.badgeId}</Text>
            </View>
          </View>

          <View style={styles.divider} />

          <Text style={styles.vehicleLabel}>Assigned Vehicle</Text>
          <View style={styles.vehicleRow}>
            <View style={styles.vehicleIconWrap}>
              <MaterialCommunityIcons name="ambulance" size={20} color={colors.textPrimary} />
            </View>
            <View>
              <Text style={styles.vehicleName}>{responderProfile.vehicle}</Text>
              <Text style={styles.vehicleType}>{responderProfile.vehicleType}</Text>
            </View>
          </View>
        </View>

        <View style={styles.statsGrid}>
          {responderStats.map((stat) => (
            <StatCard key={stat.id} stat={stat} />
          ))}
        </View>

        <View style={styles.settingsCard}>
          {settingsItems.map((item, index) => (
            <SettingsRow key={item.id} item={item} isLast={index === settingsItems.length - 1} />
          ))}
        </View>

        <TouchableOpacity style={styles.endShiftBtn} activeOpacity={0.85}>
          <Ionicons name="power" size={20} color={colors.white} />
          <View>
            <Text style={styles.endShiftTitle}>End Shift / Go Offline</Text>
            <Text style={styles.endShiftSubtitle}>You will not receive new missions</Text>
          </View>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  scrollContent: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xxxl,
  },
  profileCard: {
    backgroundColor: colors.card,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    ...shadow.card,
  },
  profileTopRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  avatar: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: colors.surfaceElevated,
  },
  profileInfo: {
    flex: 1,
    gap: 2,
  },
  nameRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    marginBottom: 2,
  },
  name: {
    ...typography.h3,
    color: colors.textPrimary,
  },
  badgeLabel: {
    ...typography.small,
    color: colors.textTertiary,
    fontWeight: '400',
    marginTop: 4,
  },
  badgeValue: {
    ...typography.bodyBold,
    color: colors.textPrimary,
  },
  divider: {
    height: 1,
    backgroundColor: colors.border,
    marginVertical: spacing.md,
  },
  vehicleLabel: {
    ...typography.small,
    color: colors.textTertiary,
    fontWeight: '400',
    marginBottom: spacing.sm,
  },
  vehicleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  vehicleIconWrap: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: colors.surfaceElevated,
    alignItems: 'center',
    justifyContent: 'center',
  },
  vehicleName: {
    ...typography.bodyBold,
    color: colors.textPrimary,
  },
  vehicleType: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.md,
    marginBottom: spacing.lg,
  },
  settingsCard: {
    backgroundColor: colors.card,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.lg,
  },
  endShiftBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    backgroundColor: colors.red,
    borderRadius: radius.lg,
    padding: spacing.lg,
  },
  endShiftTitle: {
    ...typography.bodyBold,
    color: colors.white,
  },
  endShiftSubtitle: {
    ...typography.caption,
    color: 'rgba(255,255,255,0.85)',
  },
});
