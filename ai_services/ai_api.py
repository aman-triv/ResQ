from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
from pydantic import BaseModel
import sqlite3
from ai_services import deduplicator
import os
import tempfile
import shutil
from ai_services.vision_engine import process_disaster_image
from ai_services.cluster_engine import cluster_incoming_incidents
from typing import List, Optional
from ai_services.ai_pipeline import (
    parse_sos_text,
    transcribe_audio,
    generate_first_aid,
    calculate_optimal_route,
    process_sos_pipeline,
)

app = FastAPI(title="LifeGrid AI Services API")

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


# 7. Real Background Worker Logic
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


# 8. Async SOS Trigger Endpoint
@app.post("/ai/process-sos-async")
def process_sos_async(data: IncidentItem, background_tasks: BackgroundTasks):
    background_tasks.add_task(real_ai_background_processing, data.dict())
    
    return {
        "status": "success",
        "message": "SOS received. Real AI processing, DBSCAN deduplication, and DB update queued in background."
    }