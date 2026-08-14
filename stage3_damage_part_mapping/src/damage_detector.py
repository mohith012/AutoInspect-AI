import sys
from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = r"C:\Users\sango\OneDrive\Desktop\Car project\cardd_model\exp\weights\best.pt"

_model = None

def load_damage_model():
    global _model
    if _model is None:
        if not Path(MODEL_PATH).is_file():
            raise FileNotFoundError(f"Model 1 not found at {MODEL_PATH}")
        _model = YOLO(MODEL_PATH)
    return _model

def detect_damages(image_path: str, conf_threshold: float = 0.25) -> list:
    """
    Detects damages using Model 1 and returns standardized outputs.
    """
    model = load_damage_model()
    results = model.predict(str(image_path), conf=conf_threshold, verbose=False)
    
    detections = []
    if not results or not results[0].boxes:
        return detections
        
    for box in results[0].boxes:
        c = int(box.cls[0])
        conf = float(box.conf[0])
        name = model.names[c]
        bbox = [round(v, 1) for v in box.xyxy[0].tolist()]
        
        detections.append({
            "damage": name,
            "confidence": round(conf, 3),
            "bbox": bbox
        })
        
    return detections
