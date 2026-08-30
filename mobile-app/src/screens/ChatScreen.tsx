import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { FontAwesome5 } from '@expo/vector-icons';
import Header from '../components/Header';
import ChatListItem from '../components/ChatListItem';
import ActionButton from '../components/ActionButton';
import { colors, spacing, typography } from '../theme/theme';
import { chatThreads, quickActions } from '../data/mockData';

export default function ChatScreen() {
  const urgentThread = chatThreads.find((t) => t.isUrgent);
  const otherThreads = chatThreads.filter((t) => !t.isUrgent);

  return (
    <View style={styles.container}>
      <Header title="Team Communications" subtitle="Online" subtitleIndicator="dot" />

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {urgentThread && (
          <>
            <View style={styles.sectionLabelRow}>
              <FontAwesome5 name="thumbtack" size={12} color={colors.red} solid />
              <Text style={styles.pinnedLabel}>PINNED & URGENT</Text>
            </View>
            <ChatListItem thread={urgentThread} />
          </>
        )}

        <Text style={styles.sectionLabel}>ALL CHATS</Text>
        {otherThreads.map((thread) => (
          <ChatListItem key={thread.id} thread={thread} />
        ))}
      </ScrollView>

      <View style={styles.bottomPanel}>
        <Text style={styles.quickActionsLabel}>QUICK ACTIONS (ONE-TAP)</Text>
        <View style={styles.gridRow}>
          {quickActions.map((action) => (
            <ActionButton
              key={action.id}
              label={action.label}
              iconName={action.icon}
              iconSet={action.iconSet}
              color={action.color}
              variant="grid"
              filled={false}
            />
          ))}
        </View>
        <ActionButton
          label="ADMIN SOS"
          subLabel="Alert All Units & Control Room"
          iconName="alarm-light"
          iconSet="material-community"
          color={colors.red}
          variant="hero"
          style={styles.adminSosBtn}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  scrollContent: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.xs,
    paddingBottom: spacing.xl,
  },
  sectionLabelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    marginBottom: spacing.sm,
  },
  pinnedLabel: {
    ...typography.small,
    color: colors.red,
    letterSpacing: 0.5,
  },
  sectionLabel: {
    ...typography.small,
    color: colors.textTertiary,
    letterSpacing: 0.5,
    marginTop: spacing.md,
    marginBottom: spacing.sm,
  },
  bottomPanel: {
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    padding: spacing.lg,
    gap: spacing.md,
  },
  quickActionsLabel: {
    ...typography.small,
    color: colors.textTertiary,
    letterSpacing: 0.5,
  },
  gridRow: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  adminSosBtn: {
    width: '100%',
  },
});
