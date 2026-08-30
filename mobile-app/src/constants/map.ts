/**
 * Dark map styling + placeholder route data for the Home screen.
 *
 * Coordinates are real-world locality centers around Indiranagar /
 * Domlur / MG Road in Bengaluru (matching the location text in the
 * mockup) — they're just approximate locality markers for the demo,
 * not a live feed.
 *
 * NOTE on platform behaviour (see README "Maps setup" section):
 *  - Android's default MapView provider is Google Maps, so
 *    `customMapStyle` below applies directly.
 *  - iOS's default provider is Apple Maps, which has no JSON styling
 *    API — `userInterfaceStyle="dark"` (set on the MapView itself)
 *    gives native MapKit dark mode there instead.
 */

import type { MapStyleElement } from 'react-native-maps';

export const darkMapStyle: MapStyleElement[] = [
  { elementType: 'geometry', stylers: [{ color: '#1B1B1B' }] },
  { elementType: 'labels.icon', stylers: [{ visibility: 'off' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#8A8A8E' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#121212' }] },
  {
    featureType: 'administrative',
    elementType: 'geometry',
    stylers: [{ color: '#3A3A3C' }],
  },
  {
    featureType: 'poi',
    stylers: [{ visibility: 'off' }],
  },
  {
    featureType: 'road',
    elementType: 'geometry',
    stylers: [{ color: '#2A2A2C' }],
  },
  {
    featureType: 'road',
    elementType: 'geometry.stroke',
    stylers: [{ color: '#1B1B1B' }],
  },
  {
    featureType: 'road.arterial',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#8A8A8E' }],
  },
  {
    featureType: 'road.highway',
    elementType: 'geometry',
    stylers: [{ color: '#333335' }],
  },
  {
    featureType: 'transit',
    stylers: [{ visibility: 'off' }],
  },
  {
    featureType: 'water',
    elementType: 'geometry',
    stylers: [{ color: '#0F1C2E' }],
  },
  {
    featureType: 'water',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#5A6B7A' }],
  },
];

export const mapRegion = {
  latitude: 12.9721,
  longitude: 77.6412,
  latitudeDelta: 0.02,
  longitudeDelta: 0.02,
};

// Current ambulance position (blue heading marker)
export const currentPosition = {
  latitude: 12.9748,
  longitude: 77.6408,
};

// Active SOS destination (red marker, "1.2 km to destination")
export const destinationPosition = {
  latitude: 12.9701,
  longitude: 77.6421,
};

// City Hospital pin shown near MG Road
export const hospitalPosition = {
  latitude: 12.9758,
  longitude: 77.6045 + 0.035, // nudged into frame near MG Road/Indiranagar
};

// Route polyline from current position down to the SOS location
export const routeCoordinates = [
  currentPosition,
  { latitude: 12.9732, longitude: 77.6414 },
  { latitude: 12.9714, longitude: 77.6418 },
  destinationPosition,
];
