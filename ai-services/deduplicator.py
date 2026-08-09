from hospital_router import calculate_haversine_distance

def is_duplicate_incident(new_lat, new_lng, existing_incidents, threshold_meters=100):
    """
    Checks if an incident at the same location (within threshold_meters) already exists.
    """
    threshold_km = threshold_meters / 1000.0
    
    for incident in existing_incidents:
        dist = calculate_haversine_distance(new_lat, new_lng, incident["latitude"], incident["longitude"])
        if dist <= threshold_km:
            return True, incident["id"] # Duplicate found! Return parent incident ID
            
    return False, None

# --- Quick Test ---
if __name__ == "__main__":
    existing = [{"id": "SOS-1001", "latitude": 28.6139, "longitude": 77.2090}]
    
    # Incident reported 20 meters away
    is_dup, parent_id = is_duplicate_incident(28.6140, 77.2091, existing, threshold_meters=100)
    print(f"Is Duplicate: {is_dup}, Parent ID: {parent_id}")
