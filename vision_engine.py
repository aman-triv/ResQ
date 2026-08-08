import cv2
from ultralytics import YOLO

# Pre-trained YOLOv8 Model
model = YOLO('yolov8n.pt')

# COCO Classes mapping for disaster scenarios
DAMAGE_CLASSES = ['car', 'bus', 'truck', 'fire', 'boat']
ANIMAL_CLASSES = ['cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear']

def process_disaster_image(image_path):
    """
    Analyzes an uploaded image and returns structured JSON 
    with severity score, object tags, and rescue category.
    """
    results = model(image_path)
    
    detected_tags = []
    has_human = False
    has_animal = False
    has_damage_element = False
    
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])
            
            if confidence > 0.35: # 35% Confidence threshold
                detected_tags.append(class_name)
                
                if class_name == 'person':
                    has_human = True
                elif class_name in ANIMAL_CLASSES:
                    has_animal = True
                elif class_name in DAMAGE_CLASSES:
                    has_damage_element = True

    # --- SEVERITY SCORE CALCULATION LOGIC ---
    base_severity = 3
    if has_human:
        base_severity += 3
    if has_animal:
        base_severity += 2
    if has_damage_element:
        base_severity += 2
    if 'fire' in detected_tags:
        base_severity += 3
        
    severity_score = min(base_severity, 10) # Cap at 10

    # Category Routing
    if has_animal and not has_human:
        category = "animal"
    elif has_human:
        category = "human"
    else:
        category = "infrastructure"

    return {
        "vision_severity_score": severity_score,
        "category": category,
        "detected_objects": list(set(detected_tags)),
        "is_animal_rescue": has_animal,
        "is_human_rescue": has_human,
        "requires_medical": severity_score >= 6
    }

# --- Quick Test ---
if __name__ == "__main__":
    # Test file path
    res = process_disaster_image("test.jpg")
    print("Vision Engine Output:", res)
