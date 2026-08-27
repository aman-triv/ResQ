import math
from typing import List, Dict, Any

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates straight line distance between two GPS coordinates in kilometers."""
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def find_nearest_capable_facility(victim_lat: float, victim_lng: float, is_animal: bool, requires_icu: bool, facilities_db: List[Dict[str, Any]]):
    """
    Filters facilities based on victim requirement and returns the closest capable hospital/vet.
    """
    capable_facilities = []

    for facility in facilities_db:
        # Filter for Animals vs Humans
        if is_animal and not facility.get("is_vet_clinic", False):
            continue
        if not is_animal and facility.get("is_vet_clinic", False):
            continue
        
        # Filter for Critical ICU requirement
        if requires_icu and not facility.get("has_icu", False):
            continue

        # Calculate distance
        dist = calculate_haversine_distance(victim_lat, victim_lng, facility["lat"], facility["lng"])
        facility_copy = facility.copy()
        facility_copy["distance_km"] = dist
        capable_facilities.append(facility_copy)

    # Sort by nearest distance
    capable_facilities.sort(key=lambda x: x["distance_km"])
    
    return capable_facilities[0] if capable_facilities else None


# --- GEOJSON ROUTE GENERATOR ---

def build_geojson_route(waypoints: List[List[float]], route_name: str = "Emergency Route") -> Dict[str, Any]:
    """
    Coordinates array [[lat, lng], [lat, lng]...] ko standard GeoJSON FeatureCollection mein convert karta hai.
    Note: GeoJSON standard mein order [longitude, latitude] hota hai!
    """
    if not waypoints:
        return {"type": "FeatureCollection", "features": []}

    # GeoJSON expects [lng, lat]
    geojson_coords = [[coord[1], coord[0]] for coord in waypoints]

    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": geojson_coords
            },
            "properties": {
                "name": route_name,
                "total_waypoints": len(waypoints)
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": geojson_coords[0]
            },
            "properties": {"title": "Start / Victim Location", "type": "origin"}
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": geojson_coords[-1]
            },
            "properties": {"title": "Destination Facility", "type": "destination"}
        }
    ]

    return {
        "type": "FeatureCollection",
        "features": features
    }


# --- Quick Test ---
if __name__ == "__main__":
    dummy_facilities = [
        {"id": 1, "name": "City Human Hospital", "lat": 28.6200, "lng": 77.2100, "is_vet_clinic": False, "has_icu": True},
        {"id": 2, "name": "Paws & Claws Vet Care", "lat": 28.6150, "lng": 77.2050, "is_vet_clinic": True, "has_icu": False},
    ]
    
    victim_lat, victim_lng = 28.6139, 77.2090
    best_match = find_nearest_capable_facility(victim_lat, victim_lng, is_animal=True, requires_icu=False, facilities_db=dummy_facilities)
    print("Nearest Capable Facility:", best_match)

    if best_match:
        # Route points: Victim -> Hospital
        route_points = [[victim_lat, victim_lng], [best_match["lat"], best_match["lng"]]]
        geojson_route = build_geojson_route(route_points, f"Route to {best_match['name']}")
        print("\nGenerated GeoJSON Route:", geojson_route)
