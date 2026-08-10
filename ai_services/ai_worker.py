from celery import Celery
import time

# Redis Broker setup (Localhost par Redis chal raha hai)
celery_app = Celery(
    'ai_worker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task(name='process_sos_task')
def process_sos_task(sos_id: int, description: str):
    try:
        # 1. AI Logic / Analysis (Urgency score & animal detection)
        urgency_score = 9 if "fire" in description.lower() or "blood" in description.lower() else 5
        is_animal = "dog" in description.lower() or "cow" in description.lower() or "cat" in description.lower()
        
        # 2. Database Update (lifgrid.db mein result save karna)
        conn = sqlite3.connect('lifgrid.db')
        cursor = conn.cursor()
        
        # Assume table ka naam 'sos_requests' hai jisme ye fields hain
        cursor.execute("""
            UPDATE sos_requests 
            SET urgency_score = ?, is_animal = ?, status = 'processed' 
            WHERE id = ?
        """, (urgency_score, is_animal, sos_id))
        
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "sos_id": sos_id,
            "urgency_score": urgency_score,
            "is_animal": is_animal
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    # Celery App Configuration
celery_app = Celery(
    'ai_worker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task(name="process_sos_incident")
def process_sos_task(incident_data):
    """
    Yeh background task Redis Queue se data pick karega aur AI models ko run karega.
    """
    print(f"🚀 Naya SOS Incident Queue se pick kiya: {incident_data}")
    
    # Simulation delay
    time.sleep(2) 
    
    result = {
        "incident_id": incident_data.get("id"),
        "status": "AI Processing Completed",
        "urgency_score": 8,
        "is_animal_related": False
    }
    
    print(f"✅ Processing Done: {result}")
    return result