"""
s2_predict.py
-------------
STAGE 2 — Model 2: Vehicle Part Detection inference function.

Returns structured machine-readable results (not print statements).

Usage:
    python scripts/s2_predict.py <image_path>

Or import and call:
    from scripts.s2_predict import detect_vehicle_parts
    results = detect_vehicle_parts("car.jpg")
"""
import sys
from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = r'C:\Users\sango\OneDrive\Desktop\Car project\stage2_vehicle_part_detection\models\vehicle_parts_v1\weights\best.pt'

# Class 18 'object' is a catch-all with no meaning — excluded from output
EXCLUDED_CLASSES = {'object'}

# Project-level class mapping (dataset name → human-readable project name)
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
    'object':            'EXCLUDED',
}

_model = None

def load_model():
    global _model
    if _model is None:
        _model = YOLO(MODEL_PATH)
    return _model


def detect_vehicle_parts(image_path: str, conf_threshold: float = 0.25) -> list:
    """
    Detect vehicle parts in an image.

    Args:
        image_path: Path to the image file.
        conf_threshold: Minimum confidence to include a detection.

    Returns:
        List of dicts:
        [
            {
                "part":       "front_bumper",   # project-level name
                "raw_class":  "front_bumper",   # original dataset class
                "confidence": 0.94,
                "bbox":       [x1, y1, x2, y2]  # absolute pixels
            },
            ...
        ]
        Sorted by confidence descending.
        Class 'object' is excluded.
    """
    model = load_model()
    results = model.predict(str(image_path), conf=conf_threshold, verbose=False)

    detections = []
    if not results or not results[0].boxes:
        return detections

    boxes = results[0].boxes
    for box in boxes:
        cls_id   = int(box.cls[0])
        raw_name = model.names[cls_id]

        if raw_name in EXCLUDED_CLASSES:
            continue

        conf = float(box.conf[0])
        x1, y1, x2, y2 = [round(v, 1) for v in box.xyxy[0].tolist()]
        project_name = CLASS_MAP.get(raw_name, raw_name)

        detections.append({
            "part":       project_name,
            "raw_class":  raw_name,
            "confidence": round(conf, 3),
            "bbox":       [x1, y1, x2, y2]
        })

    detections.sort(key=lambda d: d["confidence"], reverse=True)
    return detections


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/s2_predict.py <image_path>")
        sys.exit(1)

    img = sys.argv[1]
    print(f"\n=== Model 2 — Vehicle Part Detection ===")
    print(f"Image : {img}")
    print(f"Model : {MODEL_PATH}")
    print("-" * 45)

    parts = detect_vehicle_parts(img)

    if not parts:
        print("No vehicle parts detected.")
    else:
        print(f"Detected {len(parts)} part(s):\n")
        for i, d in enumerate(parts, 1):
            print(f"  [{i}] {d['part']:<20} {d['confidence']*100:.1f}%  bbox: {d['bbox']}")
    print("=" * 45)
