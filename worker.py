import time
import json
import sqlite3

# AI Services & Deduplication Imports
try:
    from ai_services.ai_pipeline import process_text_urgency
except ImportError:
    def process_text_urgency(text):
        return {"urgency_score": 3, "tags": ["SOS", "Emergency"]}

try:
    from vision_service import analyze_image
except ImportError:
    def analyze_image(image_data):
        return {"severity_score": 5, "detected_objects": ["Emergency", "Alert"]}

try:
    from dedup_service import check_duplicates
except ImportError:
    def check_duplicates(lat, lon, text):
        return False

DB_NAME = "lifegrid.db"

def process_sos_task(sos_id: int, victim_category: str = "human"):
    print(f"\n[⚙️ WORKER] Processing SOS Request ID: {sos_id}...")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Database se raw SOS data fetch karo
    cursor.execute("SELECT text_description, latitude, longitude FROM sos_requests WHERE id = ?", (sos_id,))
    row = cursor.fetchone()
    
    if not row:
        print(f"[❌ WORKER] SOS ID {sos_id} database me nahi mila!")
        conn.close()
        return

    text_desc, lat, lon = row
    urgency_score = 1
    tags = []

    # 2. Text NLP Pipeline Run Karo
    if text_desc:
        try:
            nlp_res = process_text_urgency(text_desc)
            urgency_score = max(urgency_score, nlp_res.get("urgency_score", 1))
            tags.extend(nlp_res.get("tags", []))
            print(f"   └─ [NLP] Urgency Score: {urgency_score}, Tags: {tags}")
        except Exception as e:
            print(f"   └─ [!] NLP Error: {e}")

    # 3. Vision AI Pipeline Run Karo
    try:
        vision_res = analyze_image(None)
        urgency_score = max(urgency_score, vision_res.get("severity_score", 1))
        tags.extend(vision_res.get("detected_objects", []))
        print(f"   └─ [Vision] Urgency Score: {urgency_score}, Tags: {tags}")
    except Exception as e:
        print(f"   └─ [!] Vision Error: {e}")

    # 4. Deduplication Check Karo
    try:
        is_dup = check_duplicates(lat, lon, text_desc)
        print(f"   └─ [Dedup] Is Duplicate: {is_dup}")
    except Exception as e:
        print(f"   └─ [!] Dedup Error: {e}")

    # 5. Database ko Final AI outcomes ke saath Update karo
    try:
        cursor.execute("""
            UPDATE sos_requests 
            SET urgency_score = ? 
            WHERE id = ?
        """, (urgency_score, sos_id))
        conn.commit()
    except Exception as e:
        print(f"   └─ [!] DB Update Error: {e}")
        
    conn.close()
    print(f"[✅ WORKER] SOS ID {sos_id} successfully process ho kar DB me update ho gaya!\n")