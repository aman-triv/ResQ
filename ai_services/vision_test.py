import cv2
from ultralytics import YOLO

# Pre-trained YOLOv8 Nano model load kar rahe hain (Fastest & Lightweight)
model = YOLO('yolov8n.pt')

# Common Animal Classes in COCO Dataset
ANIMAL_CLASSES = ['cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']

def analyze_image(image_path):
    # Model run karo image par
    results = model(image_path)
    
    detected_objects = []
    has_human = False
    has_animal = False
    
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])
            
            # Sirf 40%+ confidence wale detections consider karenge
            if confidence > 0.40:
                detected_objects.append({
                    "class": class_name,
                    "confidence": round(confidence, 2)
                })
                
                if class_name == 'person':
                    has_human = True
                elif class_name in ANIMAL_CLASSES:
                    has_animal = True

    # Category Decision Logic
    if has_human and has_animal:
        category = "both"
    elif has_animal:
        category = "animal"
    elif has_human:
        category = "human"
    else:
        category = "general_damage"

    return {
        "detected_objects": detected_objects,
        "category": category,
        "has_human": has_human,
        "has_animal": has_animal
    }

# --- TESTING ---
if __name__ == "__main__":
    # Yahan apni kisi bhi local test image ka path dalo
    test_image = "test.jpg" 
    try:
        output = analyze_image(test_image)
        print("=== Vision AI Analysis Output ===")
        print(output)
    except Exception as e:
        print(f"Error analyzing image: {e}")
        print("Tip: Make sure 'test.jpg' exists in the same folder.")
