import os
import cv2
import uuid
import shutil
import numpy as np
from PIL import Image
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="ResQGrid Vision AI Service")

# Static directory for serving annotated images to frontend
STATIC_DIR = "static/annotated"
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

print("Loading YOLOv8 Model...")
model = YOLO("yolov8n.pt")

TEMP_DIR = "./temp_images"
os.makedirs(TEMP_DIR, exist_ok=True)

ANIMAL_CLASSES = [15, 16, 17, 18, 19, 20, 21, 22, 23]
HUMAN_CLASS = 0

def compress_image(image_path):
    """Pillow (PIL) integration for image compression/resizing"""
    with Image.open(image_path) as img:
        img.thumbnail((800, 800)) 
        img.save(image_path, optimize=True, quality=85)

def analyze_and_annotate_image(image_path: str):
    try:
        # Pillow Compression first
        compress_image(image_path)
        
        # YOLO Inference
        results = model(image_path, verbose=False)
        img = cv2.imread(image_path)
        
        detected_threats = []
        bounding_boxes = []
        has_animal, has_human = False, False
        max_confidence = 0.0

        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                if conf > max_confidence:
                    max_confidence = conf

                if cls_id in ANIMAL_CLASSES:
                    has_animal = True
                if cls_id == HUMAN_CLASS:
                    has_human = True

                detected_threats.append(label)

                # Determine Bounding Box Color (Red for Human/Fire, Yellow for Animals/Others)
                color = (0, 0, 255) if cls_id == HUMAN_CLASS or label == 'fire' else (0, 255, 255)
                
                # Draw Box using OpenCV
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                cv2.putText(img, f"{label} {int(conf*100)}%", (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                bounding_boxes.append({
                    "label": label,
                    "confidence": round(conf, 2),
                    "box": [x1, y1, x2, y2]
                })

        # HSV Fire Detection Logic
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        fire_mask = cv2.inRange(hsv, (18, 50, 50), (35, 255, 255))
        fire_ratio = (cv2.countNonZero(fire_mask) / (img.shape[0] * img.shape[1])) * 100
        
        if fire_ratio > 2.0 and 'fire' not in detected_threats:
            detected_threats.append("fire_detected_hsv")

        # Severity Logic
        severity_score = 3
        if has_human: severity_score += 3
        if has_animal: severity_score += 2
        if fire_ratio > 10.0: severity_score += 3
        
        severity_score = min(10, severity_score)

        if severity_score >= 8:
            severity_level, pin_color = "CRITICAL", "RED"
        elif severity_score >= 5:
            severity_level, pin_color = "MEDIUM", "YELLOW"
        else:
            severity_level, pin_color = "LOW", "GREEN"

        # Save Annotated Image safely using uuid
        file_id = f"{uuid.uuid4()}.jpg"
        save_path = os.path.join(STATIC_DIR, file_id)
        cv2.imwrite(save_path, img)

        # Final JSON Layout matching specs
        return {
            "detected_threats": list(set(detected_threats)) if detected_threats else ["Clear"],
            "confidence": round(max_confidence * 100, 1),
            "severity_level": severity_level,
            "pin_color": pin_color,
            "annotated_image_url": f"/static/annotated/{file_id}",
            "bounding_boxes": bounding_boxes,
            "extra_data": {
                "category": "animal" if (has_animal and not has_human) else "human",
                "fire_intensity_percent": round(fire_ratio, 2)
            }
        }
    except Exception as e:
        print(f"Error in Vision Analysis: {e}")
        raise e

@app.post("/api/v1/analyze-image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    try:
        temp_path = os.path.join(TEMP_DIR, file.filename)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        analysis_result = analyze_and_analyze_image_helper_alias if False else analyze_and_annotate_image(temp_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
