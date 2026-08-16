import sys
import os
import time
from pathlib import Path
from PIL import Image

# Ensure the root project directory is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
stage3_path = os.path.join(project_root, "stage3_damage_part_mapping")
if stage3_path not in sys.path:
    sys.path.insert(0, stage3_path)

from src.damage_detector import detect_damages
from src.part_detector import detect_parts
from src.matcher import match_damages_to_parts

stage4_src_path = os.path.join(project_root, "stage4_severity_estimation", "src")
if stage4_src_path not in sys.path:
    sys.path.insert(0, stage4_src_path)
    
import inference
SeverityPredictor = inference.SeverityPredictor

# Initialize the Severity Predictor once globally (or inject it)
# Assuming models/severity_model_best.pt exists in stage4
SEVERITY_MODEL_PATH = os.path.join(project_root, "stage4_severity_estimation", "models", "severity_model_best.pt")
SEVERITY_THRESHOLD = 0.40

# Lazy initialization
_severity_predictor = None

def get_severity_predictor():
    global _severity_predictor
    if _severity_predictor is None:
        _severity_predictor = SeverityPredictor(SEVERITY_MODEL_PATH, threshold=SEVERITY_THRESHOLD)
    return _severity_predictor

def extract_damage_crop(image, bbox, padding_ratio=0.15, save_path=None):
    """
    Extracts a padded crop of the damage region from the original image.
    """
    img_width, img_height = image.size
    x1, y1, x2, y2 = bbox
    
    width = x2 - x1
    height = y2 - y1
    pad_w = int(width * padding_ratio)
    pad_h = int(height * padding_ratio)
    
    crop_x1 = max(0, x1 - pad_w)
    crop_y1 = max(0, y1 - pad_h)
    crop_x2 = min(img_width, x2 + pad_w)
    crop_y2 = min(img_height, y2 + pad_h)
    
    crop = image.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    
    if save_path:
        crop.save(save_path)
        
    return crop

stage6_path = os.path.join(project_root, "stage6_decision_engine", "src")
if stage6_path not in sys.path:
    sys.path.insert(0, stage6_path)
import decision_engine
engine = decision_engine.DecisionEngine()

def analyze_vehicle_damage(image_path: str, save_crops=True):
    """
    Master pipeline:
    1. Model 1 (Damages)
    2. Model 2 (Parts)
    3. Stage 3 (Damage-to-Part Mapping)
    4. Model 4 (Severity on each mapped damage crop)
    5. Stage 6 (Decision Engine)
    """
    t_start = time.time()
    
    # Check if image exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    image_name = os.path.basename(image_path)
    
    # 1. Run Damage Detection
    t_m1_start = time.time()
    damages = detect_damages(image_path, conf_threshold=0.25)
    t_m1_end = time.time()
    
    # 2. Run Part Detection
    t_m2_start = time.time()
    parts = detect_parts(image_path, conf_threshold=0.25)
    t_m2_end = time.time()
    
    # 3. Match
    t_map_start = time.time()
    mapped_damages = match_damages_to_parts(damages, parts, min_iou_threshold=0.3)
    t_map_end = time.time()
    
    # 4. Severity Estimation
    t_m3_start = time.time()
    predictor = get_severity_predictor()
    
    final_damages = []
    
    try:
        original_img = Image.open(image_path).convert("RGB")
    except Exception as e:
        original_img = None
        print(f"Failed to load image for cropping: {e}")
        
    crop_dir = os.path.join(project_root, "stage5_full_pipeline", "results", "severity_crops")
    os.makedirs(crop_dir, exist_ok=True)
    
    for i, d in enumerate(mapped_damages):
        severity_result = {
            "severity": "unknown",
            "severity_confidence": 0.0,
            "severity_probabilities": None
        }
        
        if original_img and "damage_bbox" in d and d["damage_bbox"]:
            crop_path = None
            if save_crops:
                crop_name = f"{os.path.splitext(image_name)[0]}_damage_{i}.jpg"
                crop_path = os.path.join(crop_dir, crop_name)
                
            crop = extract_damage_crop(original_img, d["damage_bbox"], padding_ratio=0.15, save_path=crop_path)
            
            # Predict severity
            sev_out = predictor.predict_severity(crop)
            severity_result["severity"] = sev_out["severity"]
            severity_result["severity_confidence"] = sev_out["confidence"]
            severity_result["severity_probabilities"] = sev_out.get("probabilities")

        # Construct intermediate dict schema
        final_d = {
            "damage_type": d.get("damage", "unknown"),
            "damage_confidence": d.get("damage_confidence"),
            "damaged_part": d.get("damaged_part", "unknown"),
            "part_confidence": d.get("part_confidence"),
            "mapping_score": d.get("mapping_score"),
            "severity": severity_result["severity"],
            "severity_confidence": severity_result["severity_confidence"],
            "damage_bbox": d.get("damage_bbox"),
            "part_bbox": d.get("part_bbox")
        }
        
        if severity_result.get("severity_probabilities"):
             final_d["severity_probabilities"] = severity_result["severity_probabilities"]

        final_damages.append(final_d)
        
    t_m3_end = time.time()
    
    # 5. Decision Engine
    t_de_start = time.time()
    decision_payload = engine.evaluate_vehicle(final_damages)
    t_de_end = time.time()
    
    # Performance metrics
    perf = {
        "Model 1 (ms)": round((t_m1_end - t_m1_start) * 1000, 1),
        "Model 2 (ms)": round((t_m2_end - t_m2_start) * 1000, 1),
        "Mapping (ms)": round((t_map_end - t_map_start) * 1000, 1),
        "Model 3 (ms)": round((t_m3_end - t_m3_start) * 1000, 1),
        "Decision (ms)": round((t_de_end - t_de_start) * 1000, 1),
        "Total (ms)": round((t_de_end - t_start) * 1000, 1)
    }
    
    return {
        "image": image_name,
        "performance": perf,
        "overall_recommendation": decision_payload["overall_recommendation"],
        "damages": decision_payload["damages"]
    }

if __name__ == "__main__":
    import json
    import sys
    if len(sys.argv) < 2:
        print("Usage: python src/pipeline.py <img_path>")
        sys.exit(1)
        
    result = analyze_vehicle_damage(sys.argv[1])
    print(json.dumps(result, indent=2))
