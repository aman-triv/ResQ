# ai_services/enroute_matcher.py

from shapely.geometry import LineString, Point
from ai_services.route_manager import get_all_active_routes

def check_enroute_match(sos_lat: float, sos_lng: float, max_distance_km: float = 2.0):
    """
    Naye SOS ko saari active rescue teams ke routes se check karta hai.
    Agar koi team 1-2 km radius ke paas se guzar rahi hai, toh match return karega.
    """
    sos_point = Point(sos_lat, sos_lng)
    matched_teams = []

    active_routes = get_all_active_routes()

    for team_id, waypoints in active_routes.items():
        if len(waypoints) < 2:
            continue  # Route ke liye kam se kam 2 points chahiye
        
        # Polyline create kar rahe hain
        route_line = LineString(waypoints)
        
        # Approximate distance calculation in degrees (1 degree ~ 111 km)
        distance_deg = route_line.distance(sos_point)
        distance_km = distance_deg * 111.0  

        # Agar distance 1-2 km ke andar hai
        if distance_km <= max_distance_km:
            matched_teams.append({
                "team_id": team_id,
                "distance_km": round(distance_km, 2),
                "status": "ENROUTE_AVAILABLE"
            })

    return matched_teams