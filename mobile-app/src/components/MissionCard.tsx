import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { colors, radius, shadow, spacing, typography } from '../theme/theme';
import Badge from './Badge';
import type { Mission, MissionStatus } from '../types/models';

interface MissionCardProps {
  mission: Mission;
  /** false for the last card in the list — omits the connecting line below it */
  showConnector?: boolean;
}

const STATUS_COLOR: Record<MissionStatus, string> = {
  active: colors.red,
  queued: colors.orange,
  completed: colors.green,
};

const STATUS_LABEL: Record<MissionStatus, string> = {
  active: 'ACTIVE',
  queued: 'QUEUED',
  completed: 'COMPLETED',
};

function MissionTypeIcon({ mission }: { mission: Mission }) {
  const color = STATUS_COLOR[mission.status];
  const name = mission.icon === 'pulse' ? 'pulse' : mission.icon === 'person' ? 'person' : 'checkmark';
  return (
    <View style={[styles.iconCircle, { backgroundColor: color }]}>
      <Ionicons name={name as any} size={20} color={colors.white} />
    </View>
  );
}

function DashedLine({ color }: { color: string }) {
  const dashes = Array.from({ length: 10 });
  return (
    <View style={styles.dashedLine}>
      {dashes.map((_, i) => (
        <View key={i} style={[styles.dash, { backgroundColor: color }]} />
      ))}
    </View>
  );
}

function DetailsButton({ color }: { color: string }) {
  return (
    <TouchableOpacity style={[styles.detailsBtn, { borderColor: color }]} activeOpacity={0.8}>
      <Ionicons name="document-text-outline" size={13} color={color} />
      <Text style={[styles.detailsText, { color }]}>View Details</Text>
    </TouchableOpacity>
  );
}

export default function MissionCard({ mission, showConnector = true }: MissionCardProps) {
  const statusColor = STATUS_COLOR[mission.status];
  const isActive = mission.status === 'active';
  const isCompleted = mission.status === 'completed';

  return (
    <View style={styles.row}>
      <View style={styles.timelineCol}>
        <View style={[styles.timelineDot, { backgroundColor: statusColor }]} />
        {showConnector && <View style={styles.timelineLine} />}
      </View>

      <View
        style={[
          styles.card,
          { marginBottom: showConnector ? spacing.lg : 0 },
          isActive && styles.cardActiveBorder,
        ]}
      >
        <View style={styles.headerRow}>
          <Badge label={STATUS_LABEL[mission.status]} color={statusColor} showPulse={isActive} />
          <Text style={styles.time}>{mission.timeLabel}</Text>
        </View>

        <View style={styles.bodyRow}>
          <MissionTypeIcon mission={mission} />
          <View style={styles.textCol}>
            <Text style={styles.title}>{mission.title}</Text>
            <View style={styles.locationRow}>
              <Ionicons name="location-sharp" size={12} color={colors.textSecondary} />
              <Text style={styles.location} numberOfLines={1}>
                {mission.location}
              </Text>
            </View>
          </View>
        </View>

        {isCompleted ? (
          <View style={styles.hospitalRow}>
            <MaterialCommunityIcons name="hospital-building" size={20} color={colors.textSecondary} />
            <View style={styles.hospitalTextCol}>
              <Text style={styles.hospitalName}>{mission.hospitalName}</Text>
              <Text style={styles.hospitalCaption}>{mission.statusLine}</Text>
            </View>
            <DetailsButton color={statusColor} />
          </View>
        ) : (
          <>
            <View style={styles.progressRow}>
              <View style={[styles.progressDot, { backgroundColor: colors.green }]} />
              <Text style={styles.progressLabel}>{mission.distanceLabel}</Text>
              <DashedLine color={colors.textTertiary} />
              <Ionicons name="arrow-forward" size={12} color={colors.textTertiary} />
              <View style={[styles.progressDot, { backgroundColor: statusColor }]} />
              <Text style={styles.progressLabel} numberOfLines={1}>
                {mission.destinationLabel}
              </Text>
            </View>

            <View style={styles.footerRow}>
              <View style={styles.footerLeft}>
                <Ionicons
                  name={isActive ? 'navigate-outline' : 'hourglass-outline'}
                  size={14}
                  color={colors.textSecondary}
                />
                <Text style={styles.footerText} numberOfLines={1}>
                  {mission.statusLine}
                </Text>
              </View>
              <DetailsButton color={statusColor} />
            </View>
          </>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
  },
  timelineCol: {
    width: 28,
    alignItems: 'center',
  },
  timelineDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginTop: spacing.md,
  },
  timelineLine: {
    flex: 1,
    width: 2,
    backgroundColor: colors.border,
    marginTop: 4,
  },
  card: {
    flex: 1,
    backgroundColor: colors.card,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    ...shadow.card,
  },
  cardActiveBorder: {
    borderColor: colors.red,
    borderWidth: 1.5,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
  },
  time: {
    ...typography.caption,
    color: colors.textTertiary,
  },
  bodyRow: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  iconCircle: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  textCol: {
    flex: 1,
    gap: 3,
    justifyContent: 'center',
  },
  title: {
    ...typography.bodyBold,
    color: colors.textPrimary,
  },
  locationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  location: {
    ...typography.caption,
    color: colors.textSecondary,
    flexShrink: 1,
  },
  progressRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surfaceElevated,
    borderRadius: radius.md,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.sm,
    gap: 6,
    marginBottom: spacing.md,
  },
  progressDot: {
    width: 7,
    height: 7,
    borderRadius: 3.5,
  },
  progressLabel: {
    ...typography.small,
    color: colors.textSecondary,
    flexShrink: 1,
  },
  dashedLine: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  dash: {
    width: 3,
    height: 2,
    borderRadius: 1,
  },
  hospitalRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    backgroundColor: colors.surfaceElevated,
    borderRadius: radius.md,
    padding: spacing.sm,
  },
  hospitalTextCol: {
    flex: 1,
    gap: 2,
  },
  hospitalName: {
    ...typography.bodyBold,
    color: colors.textPrimary,
  },
  hospitalCaption: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  footerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.sm,
  },
  footerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    flex: 1,
  },
  footerText: {
    ...typography.caption,
    color: colors.textSecondary,
    flexShrink: 1,
  },
  detailsBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    borderWidth: 1,
    borderRadius: radius.pill,
    paddingHorizontal: spacing.sm,
    paddingVertical: 6,
  },
  detailsText: {
    ...typography.small,
  },
});
