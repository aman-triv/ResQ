import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import MapView, { Marker, Polyline } from 'react-native-maps';
import Header from '../components/Header';
import ActionButton from '../components/ActionButton';
import SOSAlertCard from '../components/SOSAlertCard';
import { colors, radius, shadow, spacing, typography } from '../theme/theme';
import { sosAlert, vehicleInfo } from '../data/mockData';
import {
  darkMapStyle,
  mapRegion,
  currentPosition,
  destinationPosition,
  hospitalPosition,
  routeCoordinates,
} from '../constants/map';

type IconSet = 'ionicons' | 'material-community';

function InfoBarItem({
  iconName,
  iconSet = 'ionicons',
  label,
  sublabel,
}: {
  iconName: string;
  iconSet?: IconSet;
  label: string;
  sublabel: string;
}) {
  const IconComponent = iconSet === 'material-community' ? MaterialCommunityIcons : Ionicons;
  return (
    <View style={styles.infoItem}>
      <IconComponent name={iconName as any} size={18} color={colors.textSecondary} />
      <View>
        <Text style={styles.infoLabel} numberOfLines={1}>
          {label}
        </Text>
        <Text style={styles.infoSublabel} numberOfLines={1}>
          {sublabel}
        </Text>
      </View>
    </View>
  );
}

export default function HomeScreen() {
  const [alertVisible, setAlertVisible] = useState(true);

  return (
    <View style={styles.container}>
      <Header
        title="Team Alpha Active"
        titleIndicatorColor={colors.red}
        subtitle="You are on duty"
        subtitleIndicator="shield"
      />

      <View style={styles.infoBar}>
        <InfoBarItem
          iconName="ambulance"
          iconSet="material-community"
          label={vehicleInfo.vehicleId}
          sublabel={vehicleInfo.plate}
        />
        <View style={styles.infoDivider} />
        <InfoBarItem iconName="speedometer-outline" label={`${vehicleInfo.speedKmh} km/h`} sublabel="Current Speed" />
        <View style={styles.infoDivider} />
        <InfoBarItem
          iconName="navigate-outline"
          label={`${vehicleInfo.distanceToDestinationKm} km`}
          sublabel="To Destination"
        />
      </View>

      <View style={styles.mapWrap}>
        <MapView
          style={StyleSheet.absoluteFill}
          initialRegion={mapRegion}
          customMapStyle={darkMapStyle}
          userInterfaceStyle="dark"
        >
          <Polyline coordinates={routeCoordinates} strokeColor={colors.blue} strokeWidth={4} />

          <Marker coordinate={currentPosition} anchor={{ x: 0.5, y: 0.5 }}>
            <View style={styles.currentMarker}>
              <Ionicons name="navigate" size={16} color={colors.white} />
            </View>
          </Marker>

          <Marker coordinate={destinationPosition} anchor={{ x: 0.5, y: 0.5 }}>
            <View style={styles.destMarkerRing}>
              <View style={styles.destMarkerCore} />
            </View>
          </Marker>

          <Marker coordinate={hospitalPosition} anchor={{ x: 0.5, y: 0.5 }} title="City Hospital">
            <View style={styles.hospitalMarker}>
              <Text style={styles.hospitalMarkerText}>H</Text>
            </View>
          </Marker>
        </MapView>

        <TouchableOpacity style={styles.recenterPill} activeOpacity={0.85}>
          <Ionicons name="locate" size={14} color={colors.textPrimary} />
          <Text style={styles.recenterText}>Re-center</Text>
        </TouchableOpacity>

        <View style={styles.zoomControls}>
          <TouchableOpacity style={[styles.zoomBtn, styles.zoomBtnBorder]} activeOpacity={0.85}>
            <Ionicons name="add" size={20} color={colors.textPrimary} />
          </TouchableOpacity>
          <TouchableOpacity style={[styles.zoomBtn, styles.zoomBtnBorder]} activeOpacity={0.85}>
            <Ionicons name="remove" size={20} color={colors.textPrimary} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.zoomBtn} activeOpacity={0.85}>
            <Ionicons name="navigate-outline" size={18} color={colors.textPrimary} />
          </TouchableOpacity>
        </View>

        <View style={styles.trafficLegend}>
          <MaterialCommunityIcons name="traffic-light" size={16} color={colors.textPrimary} />
          <View>
            <Text style={styles.trafficLabel}>Live Traffic</Text>
            <Text style={styles.trafficStatus}>Light</Text>
          </View>
        </View>

        {alertVisible && (
          <View style={styles.alertOverlay}>
            <SOSAlertCard
              alert={sosAlert}
              onAccept={() => setAlertVisible(false)}
              onIgnore={() => setAlertVisible(false)}
            />
          </View>
        )}
      </View>

      <View style={styles.bottomPanel}>
        <ActionButton label="REACHED LOCATION" iconName="checkmark-circle-outline" color={colors.green} variant="full" />
        <View style={styles.gridRow}>
          <ActionButton
            label="PICKED PATIENT"
            iconName="procedures"
            iconSet="font-awesome-5"
            color={colors.blue}
            variant="grid"
          />
          <ActionButton
            label="AT HOSPITAL"
            iconName="hospital-building"
            iconSet="material-community"
            color={colors.orange}
            variant="grid"
          />
          <ActionButton label="CAN'T RESPOND" iconName="hand-right" color={colors.red} variant="grid" />
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  infoBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    marginHorizontal: spacing.lg,
    borderRadius: radius.lg,
    padding: spacing.md,
    marginBottom: spacing.md,
    borderWidth: 1,
    borderColor: colors.border,
  },
  infoItem: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  infoDivider: {
    width: 1,
    height: 28,
    backgroundColor: colors.border,
    marginHorizontal: spacing.sm,
  },
  infoLabel: {
    ...typography.bodyBold,
    color: colors.textPrimary,
  },
  infoSublabel: {
    ...typography.small,
    color: colors.textTertiary,
    fontWeight: '400',
  },
  mapWrap: {
    flex: 1,
    overflow: 'hidden',
  },
  currentMarker: {
    width: 34,
    height: 34,
    borderRadius: 17,
    backgroundColor: colors.blue,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 3,
    borderColor: colors.white,
    ...shadow.card,
  },
  destMarkerRing: {
    width: 26,
    height: 26,
    borderRadius: 13,
    backgroundColor: 'rgba(239,68,68,0.3)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  destMarkerCore: {
    width: 14,
    height: 14,
    borderRadius: 7,
    backgroundColor: colors.red,
    borderWidth: 2,
    borderColor: colors.white,
  },
  hospitalMarker: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: colors.red,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: colors.white,
    ...shadow.card,
  },
  hospitalMarkerText: {
    color: colors.white,
    fontWeight: '700',
    fontSize: 13,
  },
  recenterPill: {
    position: 'absolute',
    top: spacing.md,
    right: spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radius.pill,
    borderWidth: 1,
    borderColor: colors.border,
    ...shadow.card,
  },
  recenterText: {
    ...typography.caption,
    color: colors.textPrimary,
    fontWeight: '600',
  },
  zoomControls: {
    position: 'absolute',
    right: spacing.md,
    top: 64,
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    overflow: 'hidden',
    ...shadow.card,
  },
  zoomBtn: {
    width: 40,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  zoomBtnBorder: {
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  trafficLegend: {
    position: 'absolute',
    left: spacing.md,
    bottom: spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    ...shadow.card,
  },
  trafficLabel: {
    ...typography.caption,
    color: colors.textPrimary,
    fontWeight: '600',
  },
  trafficStatus: {
    ...typography.small,
    color: colors.green,
    fontWeight: '600',
  },
  alertOverlay: {
    position: 'absolute',
    top: spacing.lg,
    left: spacing.lg,
    right: spacing.lg,
  },
  bottomPanel: {
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    padding: spacing.lg,
    gap: spacing.md,
  },
  gridRow: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
});
