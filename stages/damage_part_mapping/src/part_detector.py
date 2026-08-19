import sys
from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = r"C:\Users\sango\OneDrive\Desktop\Car project\stages/vehicle_part_detection\models\vehicle_parts_v1\weights\best.pt"

EXCLUDED_CLASSES = {'object'}

CLASS_MAP = {
    'back_bumper':       'rear_bumper',
    'front_bumper':      'front_bumper',
    'back_door':         'door',
    'front_door':        'door',
    'back_left_door':    'door',
    'back_right_door':   'door',
    'front_left_door':   'door',
    'front_right_door':  'door',
    'back_glass':        'rear_windshield',
    'front_glass':       'windshield',
    'back_left_light':   'taillight',
    'back_right_light':  'taillight',
    'back_light':        'taillight',
    'front_left_light':  'headlight',
    'front_right_light': 'headlight',
    'front_light':       'headlight',
    'hood':              'hood',
    'left_mirror':       'side_mirror',
    'right_mirror':      'side_mirror',
    'tailgate':          'tailgate',
    'trunk':             'trunk',
    'wheel':             'tire',
}

_model = None

def load_part_model():
    global _model
    if _model is None:
        if not Path(MODEL_PATH).is_file():
            raise FileNotFoundError(f"Model 2 not found at {MODEL_PATH}")
        _model = YOLO(MODEL_PATH)
    return _model

def detect_parts(image_path: str, conf_threshold: float = 0.25) -> list:
    """
    Detects vehicle parts using Model 2 and returns standardized outputs.
    """
    model = load_part_model()
    results = model.predict(str(image_path), conf=conf_threshold, verbose=False)
    
    detections = []
    if not results or not results[0].boxes:
        return detections
        
    for box in results[0].boxes:
        c = int(box.cls[0])
        raw_name = model.names[c]
        
        if raw_name in EXCLUDED_CLASSES:
            continue
            
        conf = float(box.conf[0])
        mapped_name = CLASS_MAP.get(raw_name, raw_name)
        bbox = [round(v, 1) for v in box.xyxy[0].tolist()]
        
        detections.append({
            "part": mapped_name,
            "raw_class": raw_name,
            "confidence": round(conf, 3),
            "bbox": bbox
        })
        
    return detections
