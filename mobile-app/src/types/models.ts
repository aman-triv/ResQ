export type MissionStatus = 'active' | 'queued' | 'completed';

export type MissionIcon = 'pulse' | 'person' | 'check';

export interface Mission {
  id: string;
  status: MissionStatus;
  timeLabel: string;
  title: string;
  location: string;
  icon: MissionIcon;
  /** Only present for active/queued missions (progress-row) */
  distanceLabel?: string;
  destinationLabel?: string;
  /** Only present for completed missions (hospital hand-off row) */
  hospitalName?: string;
  /** Footer status line, e.g. "En-Route to Patient Location" / "Handover completed" */
  statusLine: string;
}

export type ChatAvatarKind = 'dispatch' | 'medicalCross' | 'team' | 'hospital';

export interface ChatThread {
  id: string;
  name: string;
  avatarKind: ChatAvatarKind;
  avatarColor: string;
  lastMessage: string;
  timeLabel: string;
  unreadCount?: number;
  isVoiceNote?: boolean;
  voiceDuration?: string;
  isUrgent?: boolean;
}

export interface ResponderStat {
  id: string;
  label: string;
  value: string;
  sublabel: string;
  icon: string; // Ionicons glyph name
  color: string;
}

export interface SettingsItem {
  id: string;
  title: string;
  subtitle: string;
  icon: string; // Ionicons glyph name
  iconColor: string;
}

export interface SOSAlert {
  title: string;
  location: string;
  meta: string; // "Male  •  58 Yrs  •  Conscious  •  Severe Chest Pain"
  timeLabel: string;
}

export interface ResponderProfile {
  name: string;
  badgeId: string;
  vehicle: string;
  vehicleType: string;
  avatarUrl: string;
}

export interface QuickAction {
  id: string;
  label: string;
  icon: string;
  iconSet: 'ionicons' | 'material-community';
  color: string;
}
