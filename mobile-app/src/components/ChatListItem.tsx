import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons, MaterialCommunityIcons, FontAwesome5 } from '@expo/vector-icons';
import { colors, radius, shadow, spacing, typography } from '../theme/theme';
import type { ChatThread } from '../types/models';

interface ChatListItemProps {
  thread: ChatThread;
}

function AvatarIcon({ kind }: { kind: ChatThread['avatarKind'] }) {
  switch (kind) {
    case 'dispatch':
      return <MaterialCommunityIcons name="radio-tower" size={22} color={colors.white} />;
    case 'medicalCross':
      return <FontAwesome5 name="plus" size={16} color={colors.white} solid />;
    case 'hospital':
      return <MaterialCommunityIcons name="hospital-building" size={20} color={colors.white} />;
    case 'team':
    default:
      return <Ionicons name="people" size={20} color={colors.white} />;
  }
}

function MiniWaveform({ color, duration }: { color: string; duration?: string }) {
  const heights = [6, 12, 8, 15, 6];
  return (
    <View style={styles.waveformRow}>
      <Ionicons name="play" size={11} color={color} />
      <View style={styles.waveformBars}>
        {heights.map((h, i) => (
          <View key={i} style={[styles.waveformBar, { height: h, backgroundColor: color }]} />
        ))}
      </View>
      {!!duration && <Text style={[styles.waveformDuration, { color }]}>{duration}</Text>}
    </View>
  );
}

export default function ChatListItem({ thread }: ChatListItemProps) {
  return (
    <TouchableOpacity
      activeOpacity={0.8}
      style={[styles.container, thread.isUrgent && styles.urgentContainer]}
    >
      <View style={[styles.avatar, { backgroundColor: thread.avatarColor }]}>
        <AvatarIcon kind={thread.avatarKind} />
      </View>

      <View style={styles.content}>
        <View style={styles.topRow}>
          <View style={styles.nameRow}>
            <Text style={styles.name} numberOfLines={1}>
              {thread.name}
            </Text>
            {thread.isUrgent && (
              <View style={styles.urgentBadge}>
                <Text style={styles.urgentBadgeText}>URGENT</Text>
              </View>
            )}
          </View>
          <Text style={styles.time}>{thread.timeLabel}</Text>
        </View>

        <View style={styles.bottomRow}>
          {thread.isVoiceNote ? (
            <MiniWaveform color={thread.isUrgent ? colors.red : colors.textSecondary} duration={thread.voiceDuration} />
          ) : (
            <Text style={styles.message} numberOfLines={2}>
              {thread.lastMessage}
            </Text>
          )}
          {!!thread.unreadCount && (
            <View style={[styles.unreadBadge, { backgroundColor: thread.isUrgent ? colors.red : colors.green }]}>
              <Text style={styles.unreadText}>{thread.unreadCount}</Text>
            </View>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    gap: spacing.md,
    backgroundColor: colors.card,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    marginBottom: spacing.md,
  },
  urgentContainer: {
    borderColor: colors.red,
    borderWidth: 1.5,
    ...shadow.card,
  },
  avatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
  },
  content: {
    flex: 1,
    gap: 6,
  },
  topRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: spacing.sm,
  },
  nameRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    flexShrink: 1,
  },
  name: {
    ...typography.bodyBold,
    color: colors.textPrimary,
    flexShrink: 1,
  },
  urgentBadge: {
    backgroundColor: colors.red,
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: radius.sm,
  },
  urgentBadgeText: {
    ...typography.small,
    color: colors.white,
    fontSize: 9,
  },
  time: {
    ...typography.small,
    color: colors.textTertiary,
    fontWeight: '400',
  },
  bottomRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: spacing.sm,
  },
  message: {
    ...typography.caption,
    color: colors.textSecondary,
    flex: 1,
  },
  waveformRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  waveformBars: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 2,
  },
  waveformBar: {
    width: 2.5,
    borderRadius: 2,
  },
  waveformDuration: {
    ...typography.caption,
  },
  unreadBadge: {
    minWidth: 20,
    height: 20,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 5,
  },
  unreadText: {
    ...typography.small,
    color: colors.white,
  },
});
