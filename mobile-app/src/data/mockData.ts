import { colors } from '../theme/theme';
import type {
  Mission,
  ChatThread,
  ResponderStat,
  SettingsItem,
  SOSAlert,
  ResponderProfile,
  QuickAction,
} from '../types/models';

export const sosAlert: SOSAlert = {
  title: 'New En-Route SOS - Heart Attack',
  location: 'Indiranagar, 100ft Road, Bengaluru',
  meta: 'Male  •  58 Yrs  •  Conscious  •  Severe Chest Pain',
  timeLabel: 'Just now',
};

export const vehicleInfo = {
  vehicleId: 'AMB 02',
  plate: 'KA 01 AB 1234',
  speedKmh: 48,
  distanceToDestinationKm: 1.2,
};

export const missions: Mission[] = [
  {
    id: 'm1',
    status: 'active',
    timeLabel: 'Just now',
    title: 'En-Route SOS - Heart Attack',
    location: 'Indiranagar, 100ft Road, Bengaluru',
    icon: 'pulse',
    distanceLabel: '2.8 km',
    destinationLabel: 'City Hospital',
    statusLine: 'En-Route to Patient Location',
  },
  {
    id: 'm2',
    status: 'queued',
    timeLabel: '3 min ago',
    title: 'En-Route SOS - Breathing Difficulty',
    location: 'HSR Layout, Sector 2, Bengaluru',
    icon: 'person',
    distanceLabel: '5.6 km',
    destinationLabel: 'Patient Location',
    statusLine: 'Waiting for availability',
  },
  {
    id: 'm3',
    status: 'completed',
    timeLabel: '35 min ago',
    title: 'Patient Dropped at Hospital',
    location: 'Indiranagar, 100ft Road, Bengaluru',
    icon: 'check',
    hospitalName: 'City Hospital',
    statusLine: 'Handover completed',
  },
  {
    id: 'm4',
    status: 'completed',
    timeLabel: '2 hrs ago',
    title: 'Patient Dropped at Hospital',
    location: 'Koramangala, 4th Block, Bengaluru',
    icon: 'check',
    hospitalName: 'Apollo Hospitals',
    statusLine: 'Handover completed',
  },
  {
    id: 'm5',
    status: 'completed',
    timeLabel: '4 hrs ago',
    title: 'Patient Dropped at Hospital',
    location: 'Jayanagar, 9th Block, Bengaluru',
    icon: 'check',
    hospitalName: 'Narayana Health',
    statusLine: 'Handover completed',
  },
];

export const rescuesCompletedToday = missions.filter((m) => m.status === 'completed').length + 1; // +1 to match mockup's "4"

export const chatThreads: ChatThread[] = [
  {
    id: 'c0',
    name: 'Central Dispatch',
    avatarKind: 'dispatch',
    avatarColor: colors.red,
    lastMessage: 'Confirming Location C SOS…',
    timeLabel: 'Just now',
    unreadCount: 3,
    isVoiceNote: true,
    voiceDuration: '0:12',
    isUrgent: true,
  },
  {
    id: 'c1',
    name: 'City Hospital ER - Dr. Sharma',
    avatarKind: 'medicalCross',
    avatarColor: colors.green,
    lastMessage: 'Auto-Inform: En-Route SOS - Heart Attack. Confirm patient arrival in 10 mins',
    timeLabel: '2 mins ago',
    unreadCount: 2,
  },
  {
    id: 'c2',
    name: 'Team Alpha Squad',
    avatarKind: 'team',
    avatarColor: colors.blue,
    lastMessage: "Who's closer to MG Road?",
    timeLabel: '8 mins ago',
    unreadCount: 1,
    isVoiceNote: true,
    voiceDuration: '0:08',
  },
  {
    id: 'c3',
    name: 'Apollo Hospitals - Emergency Desk',
    avatarKind: 'hospital',
    avatarColor: colors.purple,
    lastMessage: 'Bed availability: 2 ICU, 1 Cardiac Unit',
    timeLabel: '15 mins ago',
    unreadCount: 1,
  },
  {
    id: 'c4',
    name: 'Night Shift Crew',
    avatarKind: 'team',
    avatarColor: colors.orange,
    lastMessage: 'Shift handover at 08:00 PM today',
    timeLabel: '1 hr ago',
    unreadCount: 3,
  },
  {
    id: 'c5',
    name: 'Greenview Medical Center',
    avatarKind: 'medicalCross',
    avatarColor: colors.teal,
    lastMessage: 'Patient admitted. Thank you.',
    timeLabel: '2 hrs ago',
  },
];

export const quickActions: QuickAction[] = [
  { id: 'q1', label: 'Heavy Traffic', icon: 'car-multiple', iconSet: 'material-community', color: colors.orange },
  { id: 'q2', label: 'Requesting Backup', icon: 'ambulance', iconSet: 'material-community', color: colors.blue },
  { id: 'q3', label: 'Need More Oxygen', icon: 'gas-cylinder', iconSet: 'material-community', color: colors.green },
];

export const responderProfile: ResponderProfile = {
  name: 'Team Alpha - Lead',
  badgeId: '#EMT-4920',
  vehicle: 'Ambulance 02',
  vehicleType: '(Advanced Life Support)',
  avatarUrl: 'https://i.pravatar.cc/300?img=12',
};

export const responderStats: ResponderStat[] = [
  { id: 's1', label: 'Rescues (Today)', value: '4', sublabel: 'Completed', icon: 'heart', color: colors.green },
  { id: 's2', label: 'Avg ETA (Today)', value: '6 mins', sublabel: 'On-Scene', icon: 'time', color: colors.blue },
  { id: 's3', label: 'Shift (Today)', value: '8AM - 8PM', sublabel: 'Active Shift', icon: 'calendar', color: colors.orange },
  { id: 's4', label: 'Distance (Today)', value: '120 km', sublabel: 'Traveled', icon: 'location', color: colors.purple },
];

export const settingsItems: SettingsItem[] = [
  { id: 'set1', title: 'Shift History', subtitle: 'View your past shifts and reports', icon: 'clipboard-outline', iconColor: colors.green },
  { id: 'set2', title: 'Emergency Medical Protocols', subtitle: 'Access protocols & treatment guides', icon: 'book-outline', iconColor: colors.red },
  { id: 'set3', title: 'App Settings', subtitle: 'Notifications, Appearance, Preferences', icon: 'settings-outline', iconColor: colors.blue },
  { id: 'set4', title: 'Help & Support', subtitle: 'FAQs, Contact Support, Feedback', icon: 'help-circle-outline', iconColor: colors.purple },
];
