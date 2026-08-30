# Emergency Rescue Team App

Cross-platform (iOS & Android) frontend for a paramedic/ambulance dispatch app, built with
Expo + React Native + TypeScript. Implements 4 screens — Home (live map + SOS alerts), Jobs
(mission timeline), Chat (team communications), Profile (responder details) — matching the
provided dark-mode mockups.

## Tech stack

| Concern | Library | Version installed |
|---|---|---|
| Framework | Expo (managed) | ~57.0.18 |
| Language | TypeScript | ~6.0.3 |
| UI | React Native `StyleSheet` (strict dark theme, no NativeWind) | React Native 0.86.3 / React 19.2.3 |
| Navigation | React Navigation — Bottom Tabs | @react-navigation/native ^7.3.18, @react-navigation/bottom-tabs ^7.18.18 |
| Maps | react-native-maps | ^1.29.0 |
| Icons | @expo/vector-icons (Ionicons / MaterialCommunityIcons / FontAwesome5) | ^15.1.1 |
| Gradients | expo-linear-gradient | ~57.0.1 |

All versions above were resolved directly against the npm registry for this Expo SDK — if you
add more native packages later, prefer `npx expo install <package>` so Expo can re-verify
compatibility for whatever SDK you're on by then.

## Getting started

```bash
npm install
npx expo start
```

Then press `i` for the iOS simulator, `a` for an Android emulator, or scan the QR code with
Expo Go on a physical device.

## Maps setup (read this before demoing on a real device)

`react-native-maps` needs a Google Maps API key to work fully on Android, and for a fully
custom-styled dark map on iOS. Two placeholders are already wired up in `app.json`:

```jsonc
"ios": { "config": { "googleMapsApiKey": "YOUR_IOS_GOOGLE_MAPS_API_KEY" } },
"android": { "config": { "googleMaps": { "apiKey": "YOUR_ANDROID_GOOGLE_MAPS_API_KEY" } } }
```

Get keys from the [Google Cloud Console](https://console.cloud.google.com/google/maps-apis)
(enable "Maps SDK for Android" / "Maps SDK for iOS") and drop them in.

**Platform behaviour without a key, out of the box:**
- **Android** — default provider is already Google Maps, so the custom dark JSON style in
  `src/constants/map.ts` applies directly, even in Expo Go.
- **iOS** — default provider is Apple Maps in Expo Go, which has no JSON styling API. The app
  sets `userInterfaceStyle="dark"` on the `MapView`, which gives native MapKit dark mode instead
  — so it still looks correct, just via a different mechanism than Android.
- For a **fully custom Google-styled dark map on iOS**, you'd need an EAS/dev-client build with
  the iOS key configured — plain Expo Go can't do this. Not required for demoing the UI.

## Project structure

```
App.tsx                      # NavigationContainer, dark nav theme, StatusBar
app.json                     # Expo config (dark userInterfaceStyle, Maps API key slots)
src/
  theme/theme.ts             # Colors, spacing, radius, typography, shadows — single source of truth
  types/
    models.ts                # Mission, ChatThread, ResponderStat, SettingsItem, SOSAlert, etc.
    navigation.ts             # RootTabParamList
  constants/map.ts            # Dark Google-Maps style JSON + placeholder Bengaluru coordinates
  data/mockData.ts            # All placeholder content, mirroring the mockups' exact text
  components/
    Header.tsx                # Hamburger + title/status + walkie-talkie icon (reused on all 4 screens)
    CustomTabBar.tsx           # Bottom tab bar, green active state
    ActionButton.tsx           # 3 variants: full-width row / grid / hero (covers every button in the mocks)
    SOSAlertCard.tsx           # Red gradient SOS popup with Accept/Ignore
    MissionCard.tsx            # Jobs screen timeline card (active/queued/completed states)
    ChatListItem.tsx           # Chat row incl. voice-note waveform + urgent styling
    StatCard.tsx                # Profile 2x2 stat grid card
    SettingsRow.tsx             # Profile settings list row
    Badge.tsx / PulseDot.tsx    # Status pill + the ACTIVE badge's pulsing radar-ping animation
  navigation/RootNavigator.tsx # createBottomTabNavigator wiring
  screens/
    HomeScreen.tsx             # Map, vehicle info bar, SOS overlay, bottom action panel
    JobsScreen.tsx              # Daily summary card + mission timeline
    ChatScreen.tsx               # Pinned urgent thread, chat list, sticky quick actions + Admin SOS
    ProfileScreen.tsx            # Responder card, stats grid, settings, End Shift button
```

## Notes on placeholder data

- All mission/chat/stat content in `src/data/mockData.ts` mirrors the exact text from the
  mockups (locations, names, timestamps, badge counts).
- The profile photo uses a placeholder headshot from `i.pravatar.cc` — swap
  `responderProfile.avatarUrl` in `mockData.ts` for a real asset when ready.
- Map coordinates in `src/constants/map.ts` are real Bengaluru locality centers (Indiranagar,
  MG Road, Domlur) used only for visual placement — not a live feed.
- The Jobs screen date (`"29 August 2026, Saturday"`-style) is computed live via `Date()`
  rather than hardcoded, so it won't go stale like the mockup's fixed "21 May 2025" did.

## Known follow-ups (not in scope for this pass)

- Wire up real state/navigation for Accept/Ignore, status buttons, and settings rows (currently
  presentational — `onPress` handlers are stubbed or absent where the mock has no destination).
- Hook `MissionCard` "View Details" into a detail screen/modal.
- Replace mock data with real API/socket data.
