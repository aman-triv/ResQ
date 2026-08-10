import math
import numpy as np
from sklearn.cluster import DBSCAN

def cluster_incoming_incidents(incidents_list, max_distance_meters=150):
    """
    Groups incidents occurring within max_distance_meters of each other using DBSCAN.
    """
    if not incidents_list:
        return []

    # Convert Lat/Lng to radians for Haversine distance in DBSCAN
    coords = np.array([[math.radians(inc["latitude"]), math.radians(inc["longitude"])] for inc in incidents_list])
    
    # 6371000 meters = Earth radius in meters
    kms_per_radian = 6371000.0
    epsilon = max_distance_meters / kms_per_radian

    # Run DBSCAN Spatial Clustering
    db = DBSCAN(eps=epsilon, min_samples=1, metric='haversine').fit(coords)
    labels = db.labels_

    clusters = {}
    for idx, cluster_id in enumerate(labels):
        cluster_id = int(cluster_id)
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(incidents_list[idx])

    # Consolidate each cluster into a single ticket with total report count
    summarized_tickets = []
    for cluster_id, items in clusters.items():
        # Pick the one with highest urgency score as primary incident
        primary_incident = max(items, key=lambda x: x["urgency_score"]).copy()
        primary_incident["duplicate_report_count"] = len(items)
        primary_incident["cluster_id"] = f"CLUSTER-{cluster_id + 1}"
        summarized_tickets.append(primary_incident)

    return summarized_tickets

# --- Testing Task 2 ---
if __name__ == "__main__":
    print("\n--- Clustering Engine Test ---")
    # 3 Incident reports close to each other (within ~50 meters)
    raw_sos_feed = [
        {"id": "SOS-1", "latitude": 28.61390, "longitude": 77.20900, "urgency_score": 7, "text": "Fire in building"},
        {"id": "SOS-2", "latitude": 28.61392, "longitude": 77.20905, "urgency_score": 9, "text": "Trapped on 2nd floor fire"},
        {"id": "SOS-3", "latitude": 28.61388, "longitude": 77.20898, "urgency_score": 5, "text": "Smoke seen near street"},
        # 1 Incident far away (2 km away)
        {"id": "SOS-4", "latitude": 28.63000, "longitude": 77.22000, "urgency_score": 6, "text": "Waterlogging"}
    ]

    consolidated = cluster_incoming_incidents(raw_sos_feed, max_distance_meters=150)
    print(f"Original SOS Count: {len(raw_sos_feed)} -> Consolidated Ticket Count: {len(consolidated)}")
    print("Cluster Ticket Output:", consolidated[0])
