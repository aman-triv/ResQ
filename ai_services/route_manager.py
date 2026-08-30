# ai_services/route_manager.py

# Active rescue teams ke routes ko temporary memory me hold karne ke liye dictionary
ACTIVE_ROUTES = {}

def set_active_route(team_id: str, waypoints: list):
    """
    OR-Tools se mile Latitude, Longitude pairs ko store karne ke liye function.
    waypoints format: [(28.7041, 77.1025), (28.7045, 77.1030), ...]
    """
    if not waypoints:
        return False
    ACTIVE_ROUTES[team_id] = waypoints
    return True

def get_active_route(team_id: str):
    """Kisi specific team ka active route retrieve karne ke liye."""
    return ACTIVE_ROUTES.get(team_id, None)

def get_all_active_routes():
    """Saari active teams ke routes ko return karega (SOS check ke liye)."""
    return ACTIVE_ROUTES

def remove_active_route(team_id: str):
    """Rescue complete hone par route delete karne ke liye."""
    if team_id in ACTIVE_ROUTES:
        del ACTIVE_ROUTES[team_id]
        