import time
from vision_engine import process_disaster_image
from smart_medical_router import match_victim_to_capable_facility
from cluster_engine import cluster_incoming_incidents

def run_end_to_end_demo(test_image_path):
    print("==================================================")
    print("🚀 RESQGRID AI: PERSON 4 END-TO-END PIPELINE DEMO")
    print("==================================================")
    
    # STEP 1: Process Image via Vision Engine
    print("\n[STEP 1] Running YOLOv8 Vision Analysis on Image...")
    time.sleep(1) # Simulation delay
    vision_output = process_disaster_image(test_image_path)
    print("  └─ Vision Output:", vision_output)

    # STEP 2: Smart Medical / Vet Hospital Matching
    print("\n[STEP 2] Matching Victim to Nearest Capable Medical Facility...")
    time.sleep(1)
    is_animal = vision_output["is_animal_rescue"]
    requires_icu = vision_output["requires_medical"]
    
    # Mock Victim Coordinates (Delhi/Faridabad NCR region)
    victim_lat, victim_lng = 28.6139, 77.2090
    
    matched_hospital = match_victim_to_capable_facility(
        victim_lat, victim_lng, 
        is_animal=is_animal, 
        needs_icu=requires_icu
    )
    print(f"  └─ Target Facility Assigned: {matched_hospital['name']} ({matched_hospital['distance_km']} km away)")

    # STEP 3: Deduplication & Spatial Clustering Simulation
    print("\n[STEP 3] Simulating High-Volume SOS Stream Deduplication...")
    time.sleep(1)
    
    # Simulated 4 incoming reports around same spot
    incoming_sos_stream = [
        {"id": "SOS-901", "latitude": 28.61390, "longitude": 77.20900, "urgency_score": vision_output["vision_severity_score"]},
        {"id": "SOS-902", "latitude": 28.61392, "longitude": 77.20904, "urgency_score": 8},
        {"id": "SOS-903", "latitude": 28.61388, "longitude": 77.20898, "urgency_score": 6},
        {"id": "SOS-904", "latitude": 28.63000, "longitude": 77.22000, "urgency_score": 5} # Far away
    ]
    
    consolidated_tickets = cluster_incoming_incidents(incoming_sos_stream, max_distance_meters=150)
    print(f"  └─ Processed {len(incoming_sos_stream)} Raw SOS Requests ➔ Merged into {len(consolidated_tickets)} Primary Ticket(s).")
    print("  └─ Consolidated Ticket Cluster ID:", consolidated_tickets[0]["cluster_id"], f"(Total Merged Duplicate Reports: {consolidated_tickets[0]['duplicate_report_count']})")

    print("\n✅ PIPELINE RUN COMPLETE: Ready for Control Room Dispatch!")
    print("==================================================")

if __name__ == "__main__":
    # Test file path
    run_end_to_end_demo("test.jpg")
