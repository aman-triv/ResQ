import math
from ai_services.hospital_router import calculate_haversine_distance
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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


# --- NAYA CODE: Smart Deduplication Algorithm ---

def calculate_text_similarity(text1: str, text2: str) -> float:
    """TF-IDF & Cosine Similarity check karta hai."""
    if not text1 or not text2 or not text1.strip() or not text2.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        return float(cosine_similarity([vectors[0]], [vectors[1]])[0][0])
    except Exception:
        return 0.0


def smart_deduplicate_incidents(incidents, max_distance_m=200.0, text_sim_threshold=0.3):
    """
    Location + Context Smart Clustering Algorithm
    """
    clusters = []
    visited = set()
    max_dist_km = max_distance_m / 1000.0

    for i, inc1 in enumerate(incidents):
        if inc1["id"] in visited:
            continue
        
        cluster = {
            "ticket_id": f"TICKET-{inc1['id']}",
            "primary_incident": inc1,
            "merged_incident_ids": [inc1["id"]],
            "total_reports": 1
        }
        visited.add(inc1["id"])

        for j, inc2 in enumerate(incidents):
            if i == j or inc2["id"] in visited:
                continue

            # 1. Distance Check (hospital_router KM me return karta hai)
            dist_km = calculate_haversine_distance(
                inc1["latitude"], inc1["longitude"],
                inc2["latitude"], inc2["longitude"]
            )

            if dist_km <= max_dist_km:
                # 2. Text Context Check
                text_sim = calculate_text_similarity(
                    inc1.get("text", ""), 
                    inc2.get("text", "")
                )

                if text_sim >= text_sim_threshold or not inc2.get("text"):
                    cluster["merged_incident_ids"].append(inc2["id"])
                    cluster["total_reports"] += 1
                    visited.add(inc2["id"])

        clusters.append(cluster)

    return clusters


# --- Quick Test ---
if __name__ == "__main__":
    existing = [{"id": "SOS-1001", "latitude": 28.6139, "longitude": 77.2090, "text": "Fire in building"}]
    
    # Quick Test for Smart Deduplication
    test_incidents = [
        {"id": "SOS-1001", "latitude": 28.6139, "longitude": 77.2090, "text": "Fire in building"},
        {"id": "SOS-1002", "latitude": 28.6140, "longitude": 77.2091, "text": "Huge fire breaking out"},
        {"id": "SOS-1003", "latitude": 28.6500, "longitude": 77.2500, "text": "Flood near river"}
    ]
    print("Clustered Tickets:", smart_deduplicate_incidents(test_incidents))