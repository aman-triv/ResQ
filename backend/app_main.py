from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi import File, UploadFile
import shutil
import os
from worker import process_sos_task
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
def create_sos(sos: SOSInput, background_tasks: BackgroundTasks):
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
    
    # --- BACKGROUND TASK TRIGGER ---
    background_tasks.add_task(process_sos_task, new_id, "human")
    
    return {
        "status": "Success",
        "message": "SOS saved & background processing started",
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
# Folder ensure karne ke liye ki files kahan save hongi
UPLOAD_DIR = "temp_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/upload/file")
async def upload_victim_file(file: UploadFile = File(...)):
    # File ko local server par save karna
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "filename": file.filename,
        "file_path": file_path,
        "message": "File successfully uploaded and stored for AI pipeline!"
    }

# --- STEP 1: AUTH & SECURITY (JWT & JURISDICTION) ---
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

SECRET_KEY = "crisisgrid_super_secret_key_hackathon"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Hardcoded dummy admins for hackathon city jurisdiction
ADMIN_USERS = {
    "admin_delhi": {"username": "admin_delhi", "password": "password123", "city": "Delhi"},
    "admin_mumbai": {"username": "admin_mumbai", "password": "password123", "city": "Mumbai"}
}

@app.post("/api/auth/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = ADMIN_USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {"sub": user["username"], "city": user["city"]}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer", "jurisdiction_city": user["city"]}

def get_admin_jurisdiction(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        city: str = payload.get("city")
        if username is None or city is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return {"username": username, "city": city}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # --- STEP 2: ROSTER & ALLOTMENT APIS ---

# Mock Rescue Team Roster Database/List for Hackathon Demo
RESCUE_TEAM_ROSTER = [
    {"id": 1, "name": "Captain Vikram", "phone": "+91-9876543210", "unit": "Alpha Rescue Unit", "status": "Available", "city": "Delhi"},
    {"id": 2, "name": "Officer Rajesh", "phone": "+91-9123456789", "unit": "Bravo Medical Unit", "status": "Dispatched", "city": "Delhi"},
    {"id": 3, "name": "Inspector Amit", "phone": "+91-9988776655", "unit": "Delta Fire & Disaster", "status": "Available", "city": "Mumbai"}
]

@app.get("/api/rescue-team/roster")
async def get_rescue_team_roster(admin: dict = Depends(get_admin_jurisdiction)):
    admin_city = admin["city"]
    city_team = [team for team in RESCUE_TEAM_ROSTER if team["city"] == admin_city]
    
    return {
        "jurisdiction": admin_city,
        "total_units": len(city_team),
        "roster": city_team
    }

@app.post("/api/rescue-team/allocate")
async def allocate_rescue_team(ticket_id: int, team_id: int, admin: dict = Depends(get_admin_jurisdiction)):
    return {
        "status": "success",
        "message": f"Rescue Team ID {team_id} successfully allocated to Ticket ID {ticket_id}!",
        "allocated_by": admin["username"]
    }

# --- STEP 3: REAL-TIME WEBSOCKETS (SOCKET.IO / FASTAPI WEBSOCKET) ---
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

# Connected websocket clients ko track karne ke liye manager class
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/live-tracking")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Rescue team ya client se live GPS/Status data receive karna
            data = await websocket.receive_text()
            # Sabhi connected admin dashboards ko live broadcast karna
            await manager.broadcast(f"Live Update Broadcast: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A rescue unit disconnected from live tracking.")

        from pydantic import BaseModel
import json

# Request body define karne ke liye
class StatusUpdate(BaseModel):
    status: str

@app.put("/api/rescue-team/{team_id}/status")
async def update_team_status(team_id: int, payload: StatusUpdate):
    # 1. Socket message banaya JSON format mein
    status_message = json.dumps({
        "event": "status_updated",
        "team_id": team_id,
        "new_status": payload.status
    })

    # 2. Tere existing manager se sabhi connected clients ko broadcast kar diya
    try:
        await manager.broadcast(status_message)
    except Exception as e:
        print(f"Socket emit failed: {e}")

    # 3. Success response (Agar DB setup ho toh yahan DB update query aayegi)
    return {
        "status": "success", 
        "message": f"Team {team_id} status changed to {payload.status}"
    }

from fastapi import WebSocket
from typing import Dict, List

# 1. Chat Rooms ke liye alag se Manager
class ChatRoomManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast_to_room(self, room_id: str, message: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

chat_manager = ChatRoomManager()

# 2. Chat WebSocket Endpoint with Rooms
@app.websocket("/ws/chat/{room_id}")
async def chat_websocket_endpoint(websocket: WebSocket, room_id: str):
    await chat_manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Usi room ke baaki sabhi users ko message bhej do
            await chat_manager.broadcast_to_room(room_id, data)
    except Exception:
        chat_manager.disconnect(room_id, websocket)
        await chat_manager.broadcast_to_room(room_id, f"A user disconnected from room {room_id}")
        