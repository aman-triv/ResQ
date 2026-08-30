import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import Header from '../components/Header';
import MissionCard from '../components/MissionCard';
import { colors, radius, shadow, spacing, typography } from '../theme/theme';
import { missions, rescuesCompletedToday } from '../data/mockData';

function useToday() {
  const now = new Date();
  const datePart = now.toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' });
  const weekday = now.toLocaleDateString('en-US', { weekday: 'long' });
  return { datePart, weekday };
}

export default function JobsScreen() {
  const { datePart, weekday } = useToday();

  return (
    <View style={styles.container}>
      <Header
        title="Team Alpha Active"
        titleIndicatorColor={colors.red}
        subtitle="You are on duty"
        subtitleIndicator="shield"
      />

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <View style={styles.summaryCard}>
          <View style={styles.summaryLeft}>
            <View style={styles.countCircle}>
              <Text style={styles.countText}>{rescuesCompletedToday}</Text>
            </View>
            <View style={styles.summaryTextCol}>
              <Text style={styles.summaryTitle} numberOfLines={1}>
                Rescues Completed Today
              </Text>
              <Text style={styles.summarySubtitle} numberOfLines={1}>
                Great job, Team Alpha!
              </Text>
            </View>
          </View>
          <View style={styles.dateChip}>
            <Ionicons name="calendar-outline" size={16} color={colors.textSecondary} />
            <View>
              <Text style={styles.dateText}>{datePart}</Text>
              <Text style={styles.weekdayText}>{weekday}</Text>
            </View>
          </View>
        </View>

        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>All Missions</Text>
          <TouchableOpacity style={styles.filterBtn} activeOpacity={0.7}>
            <MaterialCommunityIcons name="filter-variant" size={16} color={colors.green} />
            <Text style={styles.filterText}>Filter</Text>
          </TouchableOpacity>
        </View>

        {missions.map((mission, index) => (
          <MissionCard key={mission.id} mission={mission} showConnector={index < missions.length - 1} />
        ))}
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
  summaryCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: colors.card,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    marginBottom: spacing.lg,
    gap: spacing.sm,
    ...shadow.card,
  },
  summaryLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    flexShrink: 1,
  },
  summaryTextCol: {
    flexShrink: 1,
    gap: 2,
  },
  countCircle: {
    width: 48,
    height: 48,
    borderRadius: 24,
    borderWidth: 2,
    borderColor: colors.green,
    alignItems: 'center',
    justifyContent: 'center',
  },
  countText: {
    ...typography.h2,
    color: colors.green,
  },
  summaryTitle: {
    ...typography.bodyBold,
    color: colors.textPrimary,
  },
  summarySubtitle: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  dateChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  dateText: {
    ...typography.caption,
    color: colors.textPrimary,
    fontWeight: '600',
  },
  weekdayText: {
    ...typography.small,
    color: colors.textTertiary,
    fontWeight: '400',
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.textPrimary,
  },
  filterBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  filterText: {
    ...typography.caption,
    color: colors.green,
    fontWeight: '600',
  },
});
