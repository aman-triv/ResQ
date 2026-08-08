import math

# Sample Database of Hospitals & Vets in System
HOSPITAL_DATABASE = [
    {
        "id": "HOSP-01",
        "name": "Apollo Emergency Care",
        "lat": 28.6150,
        "lng": 77.2090,
        "is_vet_clinic": False,
        "has_icu": True,
        "has_burn_unit": True,
        "has_trauma_center": True,
        "total_beds": 50,
        "available_beds": 12
    },
    {
        "id": "HOSP-02",
        "name": "City General Hospital",
        "lat": 28.6300,
        "lng": 77.2200,
        "is_vet_clinic": False,
        "has_icu": True,
        "has_burn_unit": False,
        "has_trauma_center": False,
        "total_beds": 30,
        "available_beds": 2
    },
    {
        "id": "VET-01",
        "name": "PetCare & Livestock Rescue Vet",
        "lat": 28.6210,
        "lng": 77.2150,
        "is_vet_clinic": True,
        "has_icu": False,
        "has_burn_unit": False,
        "has_trauma_center": True,
        "total_beds": 15,
        "available_beds": 8
    }
]

def calculate_distance_km(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in KM
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def match_victim_to_capable_facility(victim_lat, victim_lng, is_animal=False, needs_icu=False, needs_burn_unit=False):
    """
    Finds nearest hospital/vet that has available beds AND matching medical facilities.
    """
    eligible_facilities = []

    for facility in HOSPITAL_DATABASE:
        # Check bed availability
        if facility["available_beds"] <= 0:
            continue

        # Human vs Animal Filter
        if is_animal and not facility["is_vet_clinic"]:
            continue
        if not is_animal and facility["is_vet_clinic"]:
            continue

        # Capability Requirements
        if needs_icu and not facility["has_icu"]:
            continue
        if needs_burn_unit and not facility["has_burn_unit"]:
            continue

        # Calculate Distance
        dist = calculate_distance_km(victim_lat, victim_lng, facility["lat"], facility["lng"])
        facility_info = facility.copy()
        facility_info["distance_km"] = dist
        eligible_facilities.append(facility_info)

    # Sort by nearest distance
    eligible_facilities.sort(key=lambda x: x["distance_km"])

    if eligible_facilities:
        return eligible_facilities[0] # Return closest capable facility
    else:
        return None # Fallback if no matching facility found

# --- Testing Task 1 ---
if __name__ == "__main__":
    print("--- Medical Matcher Test ---")
    # Test case: Human with severe burn requiring Burn Unit & ICU
    matched_hosp = match_victim_to_capable_facility(
        victim_lat=28.6139, 
        victim_lng=77.2090, 
        is_animal=False, 
        needs_icu=True, 
        needs_burn_unit=True
    )
    print("Matched Hospital for Critical Burn Victim:", matched_hosp)
