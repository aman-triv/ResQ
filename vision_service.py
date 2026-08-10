import os
import cv2
import numpy as np
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil

app = FastAPI(title="ResQGrid Vision AI Service")

# Load pre-trained YOLOv8 Nano model for ultra-fast processing
print("Loading YOLOv8 Model...")
model = YOLO("yolov8n.pt")

TEMP_DIR = "./temp_images"
os.makedirs(TEMP_DIR, exist_ok=True)

# COCO Dataset Class IDs
ANIMAL_CLASSES = [15, 16, 17, 18, 19, 20, 21, 22, 23] # dog, cat, cow, horse, sheep, etc.
HUMAN_CLASS = 0 # person

def analyze_image_damage(image_path: str):
    """
    Analyzes uploaded image for humans, animals, and visual fire/flood intensity.
    """
    try:
        results = model(image_path, verbose=False)
        detected_classes = []
        has_animal = False
        has_human = False
        
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                detected_classes.append(cls_id)
                if cls_id in ANIMAL_CLASSES:
                    has_animal = True
                if cls_id == HUMAN_CLASS:
                    has_human = True

        # Open image with OpenCV to check color intensity for Fire/Water
        img = cv2.imread(image_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Fire/Flame Hue Range Detection
        fire_mask = cv2.inRange(hsv, (18, 50, 50), (35, 255, 255))
        fire_ratio = (cv2.countNonZero(fire_mask) / (img.shape[0] * img.shape[1])) * 100

        # Calculate Severity Score (1 to 10)
        severity_score = 3 # base score
        if has_human:
            severity_score += 3
        if has_animal:
            severity_score += 2
        if fire_ratio > 10.0:
            severity_score += 3

        severity_score = min(10, severity_score)

        return {
            "image_severity_score": severity_score,
            "has_human_detected": has_human,
            "has_animal_detected": has_animal,
            "category": "animal" if (has_animal and not has_human) else "human",
            "fire_intensity_percent": round(fire_ratio, 2)
        }
    except Exception as e:
        print(f"Error in Vision Analysis: {e}")
        return {
            "image_severity_score": 5,
            "has_human_detected": True,
            "has_animal_detected": False,
            "category": "human",
            "fire_intensity_percent": 0.0
        }

@app.post("/analyze/image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    """
    API Endpoint for Vision Analysis
    """
    try:
        temp_path = os.path.join(TEMP_DIR, file.filename)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        analysis = analyze_image_damage(temp_path)
        
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return {"success": True, "data": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Runs Vision AI Service on Port 8002
    uvicorn.run(app, host="0.0.0.0", port=8002)
