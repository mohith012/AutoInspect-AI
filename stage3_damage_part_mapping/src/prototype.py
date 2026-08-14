import sys
from pathlib import Path
from ultralytics import YOLO

# Paths
MODEL1_PATH = r"C:\Users\sango\OneDrive\Desktop\Car project\cardd_model\exp\weights\best.pt"
MODEL2_PATH = r"C:\Users\sango\OneDrive\Desktop\Car project\stage2_vehicle_part_detection\models\vehicle_parts_v1\weights\best.pt"

# Excluded classes
M2_EXCLUDED_CLASSES = {'object'}

# Class mapping for Model 2
M2_CLASS_MAP = {
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

def calculate_iou(boxA, boxB):
    # Determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # Compute the area of intersection
    interArea = max(0, xB - xA) * max(0, yB - yA)

    # Compute the area of both the prediction and ground-truth rectangles
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    # Compute the intersection over union
    iou = interArea / float(boxAArea + boxBArea - interArea) if (boxAArea + boxBArea - interArea) > 0 else 0
    return iou

def point_in_box(px, py, box):
    bx1, by1, bx2, by2 = box
    return (px >= bx1 and px <= bx2 and py >= by1 and py <= by2)

def run_prototype(image_path):
    print(f"Loading models...")
    model1 = YOLO(MODEL1_PATH)
    model2 = YOLO(MODEL2_PATH)

    print(f"\nRunning inference on {image_path}...")
    res1 = model1.predict(image_path, conf=0.25, verbose=False)
    res2 = model2.predict(image_path, conf=0.25, verbose=False)

    damages = []
    if res1 and res1[0].boxes:
        for box in res1[0].boxes:
            c = int(box.cls[0])
            conf = float(box.conf[0])
            name = model1.names[c]
            bbox = [round(v, 1) for v in box.xyxy[0].tolist()]
            damages.append({
                "damage": name,
                "confidence": conf,
                "bbox": bbox
            })

    parts = []
    if res2 and res2[0].boxes:
        for box in res2[0].boxes:
            c = int(box.cls[0])
            raw_name = model2.names[c]
            if raw_name in M2_EXCLUDED_CLASSES: continue
            conf = float(box.conf[0])
            mapped_name = M2_CLASS_MAP.get(raw_name, raw_name)
            bbox = [round(v, 1) for v in box.xyxy[0].tolist()]
            parts.append({
                "part": mapped_name,
                "confidence": conf,
                "bbox": bbox
            })

    print(f"\nDamages detected: {len(damages)}")
    for d in damages: print(f"  - {d['damage']} ({d['confidence']:.2f}) at {d['bbox']}")
    print(f"Parts detected: {len(parts)}")
    for p in parts: print(f"  - {p['part']} ({p['confidence']:.2f}) at {p['bbox']}")

    print("\n--- Matching ---")
    results = []
    for d in damages:
        dx1, dy1, dx2, dy2 = d['bbox']
        dcx = (dx1 + dx2) / 2
        dcy = (dy1 + dy2) / 2
        
        best_part = None
        best_score = -1
        
        for p in parts:
            px1, py1, px2, py2 = p['bbox']
            
            in_box = point_in_box(dcx, dcy, p['bbox'])
            center_score = 1.0 if in_box else 0.0
            
            iou = calculate_iou(d['bbox'], p['bbox'])
            
            score = 0.6 * center_score + 0.4 * iou
            
            if score > best_score:
                best_score = score
                best_part = p
                
        if best_part and best_score > 0.1: # rudimentary threshold
            print(f"Result: '{best_part['part']} -> {d['damage']}' (Score: {best_score:.2f}, IoU: {calculate_iou(d['bbox'], best_part['bbox']):.2f})")
            results.append({
                "damage": d['damage'],
                "damaged_part": best_part['part'],
                "mapping_score": best_score
            })
        else:
            print(f"Result: 'uncertain -> {d['damage']}' (No strong match)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prototype.py <img_path>")
        sys.exit(1)
    run_prototype(sys.argv[1])
