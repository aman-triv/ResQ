from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import math
import sqlite3
from datetime import datetime

app = FastAPI(title="LifeGrid Emergency API - Phase 4 Persistent Production")

DB_NAME = "lifegrid.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sos_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_description TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            urgency_score INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class SOSInput(BaseModel):
    text_description: str
    latitude: float
    longitude: float

def calculate_priority(text: str) -> int:
    text_lower = text.lower()
    high_keywords = ["fire", "trap", "trapped", "blood", "medical", "heart attack", "flood", "collapse", "severe", "aag", "paani", "khoon"]
    medium_keywords = ["food", "water", "blanket", "shelter", "khana", "ration", "madad"]
    
    for word in high_keywords:
        if word in text_lower:
            return 9
            
    for word in medium_keywords:
        if word in text_lower:
            return 5
            
    return 3

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.get("/")
def home():
    return {"status": "Online", "message": "LifeGrid Phase 4 Persistent DB Server Active"}

@app.post("/api/sos")
def create_sos(sos: SOSInput):
    urgency = calculate_priority(sos.text_description)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sos_requests (text_description, latitude, longitude, urgency_score, created_at) VALUES (?, ?, ?, ?, ?)",
        (sos.text_description, sos.latitude, sos.longitude, urgency, timestamp)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "status": "Success",
        "data": {
            "id": new_id,
            "text_description": sos.text_description,
            "latitude": sos.latitude,
            "longitude": sos.longitude,
            "urgency_score": urgency,
            "created_at": timestamp
        }
    }

@app.get("/api/sos/list")
def get_all_sos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text_description, latitude, longitude, urgency_score, created_at FROM sos_requests ORDER BY urgency_score DESC")
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "text_description": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "urgency_score": row[4],
            "created_at": row[5]
        })
    return result

@app.get("/api/sos/nearby")
def get_nearby_sos(user_lat: float, user_lon: float, radius_km: float = 10.0):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text_description, latitude, longitude, urgency_score, created_at FROM sos_requests")
    rows = cursor.fetchall()
    conn.close()
    
    nearby = []
    for row in rows:
        dist = get_distance(user_lat, user_lon, row[2], row[3])
        if dist <= radius_km:
            nearby.append({
                "id": row[0],
                "text_description": row[1],
                "latitude": row[2],
                "longitude": row[3],
                "urgency_score": row[4],
                "created_at": row[5],
                "distance_km": round(dist, 2)
            })
    
    nearby_sorted = sorted(nearby, key=lambda x: x["urgency_score"], reverse=True)
    return {"total_found": len(nearby_sorted), "nearby_requests": nearby_sorted}