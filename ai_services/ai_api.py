import os
import shutil
import sqlite3
import tempfile
from typing import List, Optional

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

# Imports from ai_services
from ai_services import deduplicator
from ai_services.ai_pipeline import (
    calculate_optimal_route,
    generate_first_aid,
    parse_sos_text,
    process_sos_pipeline,
    transcribe_audio,
)
from ai_services.cluster_engine import cluster_incoming_incidents
from ai_services.deduplicator import smart_deduplicate_incidents
from ai_services.hospital_router import build_geojson_route
from ai_services.vision_engine import process_disaster_image
from ai_services.auto_allocator import auto_allocate_rescue_teams
from fastapi import Form
from ai_services.ai_pipeline import create_unified_profile
from ai_services.route_manager import set_active_route
from ai_services.enroute_matcher import check_enroute_match

app = FastAPI(title="ResQ AI Services API")


# Request Models
class IncidentItem(BaseModel):
    id: str
    latitude: float
    longitude: float
    urgency_score: int
    text: Optional[str] = ""

class ClusterRequest(BaseModel):
    incidents: List[IncidentItem]
    max_distance_meters: Optional[float] = 150.0

class TextRequest(BaseModel):
    description: str

class FirstAidRequest(BaseModel):
    emergency_desc: str

class RouteRequest(BaseModel):
    locations: List[str]
    urgency_scores: List[int]
    distance_matrix: List[List[int]]

class GeoRouteRequest(BaseModel):
    waypoints: List[List[float]]  # Example: [[28.6139, 77.2090], [28.6150, 77.2050]]


# Root Healthcheck Endpoint
@app.get("/")
def home():
    return {"status": "success", "message": "LifeGrid AI API is running!"}


# 1. Text NLP Analysis
@app.post("/ai/analyze-text")
def analyze_text_endpoint(data: TextRequest):
    try:
        urgency_score = 9 if "fire" in data.description.lower() or "blood" in data.description.lower() else 5
        is_animal = "dog" in data.description.lower() or "cow" in data.description.lower()
        
        return {
            "status": "success",
            "urgency_score": urgency_score,
            "is_animal": is_animal,
            "extracted_tags": ["trauma" if urgency_score > 7 else "general"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2. Vision AI Endpoint (YOLOv8 Image Processing)
@app.post("/ai/analyze-image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    try:
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = process_disaster_image(temp_file_path)
        
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 3. Cluster Engine Endpoint (DBSCAN Spatial Clustering)
@app.post("/ai/cluster-incidents")
def cluster_incidents_endpoint(data: ClusterRequest):
    try:
        incidents_list = [inc.dict() for inc in data.incidents]
        result = cluster_incoming_incidents(incidents_list, data.max_distance_meters)
        return {
            "status": "success",
            "cluster_count": len(result),
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 4. Whisper Audio Transcription
@app.post("/ai/transcribe-audio")
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    try:
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file.filename)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        text = transcribe_audio(temp_file_path)
        
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return {"status": "success", "transcript": text}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 5. First Aid Generation
@app.post("/ai/first-aid")
def first_aid_endpoint(data: FirstAidRequest):
    try:
        steps = generate_first_aid(data.emergency_desc)
        return {"status": "success", "first_aid": steps}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 6. Route Optimization (VRP Solver)
@app.post("/ai/optimize-route")
def optimize_route_endpoint(data: RouteRequest):
    try:
        route = calculate_optimal_route(data.locations, data.urgency_scores, data.distance_matrix)
        return {"status": "success", "route": route}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 7. GeoJSON Route Endpoint (Zomato-style map visualization)
@app.post("/ai/generate-route-geojson")
def generate_route_geojson_endpoint(data: GeoRouteRequest):
    try:
        if len(data.waypoints) < 2:
            raise HTTPException(status_code=400, detail="Kam se kam 2 waypoints chahiye route generate karne ke liye.")
        
        geojson_data = build_geojson_route(data.waypoints)
        return {
            "status": "success",
            "geojson": geojson_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 8. Real Background Worker Logic
def real_ai_background_processing(incident_data: dict):
    incident_id = incident_data.get("id")
    description = incident_data.get("text") or incident_data.get("description", "")
    lat = incident_data.get("latitude", 0.0)
    lng = incident_data.get("longitude", 0.0)
    image_path = incident_data.get("image_path", None)
    
    print(f"🚀 [Incident #{incident_id}] Background AI & Deduplication Processing Started...")
    
    ai_results = process_sos_pipeline(
        text=description,
        image_path=image_path,
        location=(lat, lng)
    )
    
    try:
        conn = sqlite3.connect("lifgrid.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, latitude, longitude FROM sos_requests WHERE id != ?", (incident_id,))
        rows = cursor.fetchall()
        existing_incidents = [{"id": row[0], "latitude": row[1], "longitude": row[2]} for row in rows if row[1] and row[2]]
        
        is_dup, parent_id = deduplicator.is_duplicate_incident(lat, lng, existing_incidents)
        final_is_duplicate = is_dup or ai_results.get("is_duplicate", False)
        status_str = 'DUPLICATE' if final_is_duplicate else 'PROCESSED'
        
        cursor.execute("""
            UPDATE sos_requests 
            SET urgency_score = ?, 
                is_animal = ?, 
                is_duplicate = ?, 
                status = ?
            WHERE id = ?
        """, (
            ai_results.get("urgency_score", 5),
            ai_results.get("is_animal", False),
            final_is_duplicate,
            status_str,
            incident_id
        ))
        
        conn.commit()
        conn.close()
        print(f"✅ [Incident #{incident_id}] Processed! Duplicate: {final_is_duplicate}, Status: {status_str}")
        
    except Exception as e:
        print(f"❌ DB / Processing Error: {e}")


# 9. Async SOS Trigger Endpoint
@app.post("/ai/process-sos-async")
def process_sos_async(data: IncidentItem, background_tasks: BackgroundTasks):
    background_tasks.add_task(real_ai_background_processing, data.dict())
    
    return {
        "status": "success",
        "message": "SOS received. Real AI processing, DBSCAN deduplication, and DB update queued in background."
    }


# 10. Smart Deduplication Endpoint
@app.post("/ai/smart-deduplicate")
def smart_deduplicate_endpoint(data: ClusterRequest):
    try:
        incidents_list = [inc.dict() for inc in data.incidents]
        grouped_tickets = smart_deduplicate_incidents(
            incidents=incidents_list, 
            max_distance_m=data.max_distance_meters or 200.0
        )
        return {
            "status": "success",
            "total_tickets": len(grouped_tickets),
            "tickets": grouped_tickets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # --- Pydantic Models ---
class RescueTeamItem(BaseModel):
    id: str
    name: Optional[str] = "Rescue Team"
    latitude: float
    longitude: float
    vehicle_type: Optional[str] = "ambulance"
    is_available: Optional[bool] = True

class TicketAssignItem(BaseModel):
    id: str
    latitude: float
    longitude: float
    urgency_score: Optional[int] = 5
    required_vehicle: Optional[str] = "ambulance"

class AutoAssignRequest(BaseModel):
    tickets: List[TicketAssignItem]
    rescue_teams: List[RescueTeamItem]


# --- Auto Allotment Endpoint ---
@app.post("/ai/auto-assign")
def auto_assign_endpoint(data: AutoAssignRequest):
    try:
        tickets_list = [t.dict() for t in data.tickets]
        # Sirf available teams filter kar rahe hain
        teams_list = [team.dict() for team in data.rescue_teams if team.is_available]

        if not teams_list:
            raise HTTPException(status_code=400, detail="Koi available rescue team nahi milli.")

        matched_assignments = auto_allocate_rescue_teams(tickets_list, teams_list)
        return {
            "status": "success",
            "total_assigned": len(matched_assignments),
            "assignments": matched_assignments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# --- Multi-Modal Unified Profile Endpoint ---
@app.post("/ai/unified-profile")
async def unified_profile_endpoint(
    latitude: float = Form(...),
    longitude: float = Form(...),
    text: Optional[str] = Form(""),
    audio_file: Optional[UploadFile] = File(None),
    image_file: Optional[UploadFile] = File(None)
):
    try:
        temp_dir = tempfile.gettempdir()
        transcript = ""
        image_result = None

        # 1. Process Audio if uploaded
        if audio_file:
            audio_path = os.path.join(temp_dir, audio_file.filename)
            with open(audio_path, "wb") as buffer:
                shutil.copyfileobj(audio_file.file, buffer)
            transcript = transcribe_audio(audio_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)

        # 2. Process Image if uploaded
        if image_file:
            image_path = os.path.join(temp_dir, image_file.filename)
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image_file.file, buffer)
            image_result = process_disaster_image(image_path)
            if os.path.exists(image_path):
                os.remove(image_path)

        # 3. Create Unified Profile
        profile = create_unified_profile(
            lat=latitude,
            lng=longitude,
            text=text or "",
            transcript=transcript,
            image_analysis=image_result
        )

        return {
            "status": "success",
            "data": profile
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# 1. API endpoint jab naya SOS aaye toh match check karne ke liye
@app.post("/api/v1/check-enroute")
async def check_enroute_sos(sos_data: dict):
    """
    Payload: {"lat": 28.6330, "lng": 77.2200}
    """
    lat = sos_data.get("lat")
    lng = sos_data.get("lng")
    
    matches = check_enroute_match(lat, lng, max_distance_km=2.0)
    
    if matches:
        return {
            "status": "ENROUTE_MATCH_FOUND",
            "alert": True,
            "matched_teams": matches
        }
    
    return {"status": "NO_ENROUTE_TEAM", "alert": False, "matched_teams": []}