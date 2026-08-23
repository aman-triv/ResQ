import numpy as np
from sklearn.cluster import DBSCAN

def filter_capable_hospitals(hospitals_list: list, victim_category: str, needs_icu: bool = False, needs_burn: bool = False):
    """
    Filters hospital inventory to return only capable facilities (Human vs Animal, ICU, Burn Ward)
    """
    capable_hospitals = []
    
    for h in hospitals_list:
        if victim_category == "animal" and h.get("is_vet_clinic", False):
            capable_hospitals.append(h)
        elif victim_category == "human" and not h.get("is_vet_clinic", False):
            if needs_icu and not h.get("has_icu", False):
                continue
            if needs_burn and not h.get("has_burn_unit", False):
                continue
            capable_hospitals.append(h)
            
    return capable_hospitals

def cluster_duplicate_sos(sos_requests: list, distance_threshold_km: float = 0.5):
    """
    Groups nearby duplicate SOS requests (within 500m) into a single incident cluster.
    """
    if not sos_requests:
        return []

    # Extract Latitudes and Longitudes
    coords = np.array([[r['lat'], r['lng']] for r in sos_requests])
    
    # Haversine distance setup
    kms_per_radian = 6371.0088
    epsilon = distance_threshold_km / kms_per_radian

    coords_rad = np.radians(coords)
    db = DBSCAN(eps=epsilon, min_samples=1, metric='haversine').fit(coords_rad)
    
    clusters = {}
    for idx, label in enumerate(db.labels_):
        label = int(label)
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(sos_requests[idx])

    # Merge duplicate clusters
    merged_results = []
    for cluster_id, items in clusters.items():
        highest_urgency_item = max(items, key=lambda x: x.get('urgency_score', 0))
        highest_urgency_item['duplicate_count'] = len(items)
        merged_results.append(highest_urgency_item)

    return merged_results

if __name__ == "__main__":
    print("--- Deduplication Module Loaded ---")
